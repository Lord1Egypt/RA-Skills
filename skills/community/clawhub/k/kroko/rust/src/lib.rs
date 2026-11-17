//! KROKO gate: enforce the NASA-grade coding limits, comments included.
//!
//! The rules are the same ones the Python implementation enforced, checked against a
//! tree-sitter parse of the source instead of CPython's `ast`. Rust was chosen for two
//! reasons that matter for a gate run on every commit: no undefined behaviour anywhere
//! in the analyser, and a peak working set measured in single-digit megabytes where the
//! interpreter needed hundreds.
//!
//! Codes
//!     K000 the file could not be parsed
//!     K001 recursion          K002 function over 60 lines
//!     K003 nesting over 3     K004 more than 4 parameters
//!     K005 cognitive over 15  K006 blanket exception swallowed
//!     K007 module-level state K008 placeholder comment
//!     K009 commented-out code K010 banner comment
//!     K011 missing public docstring
//!     K012 docstring not a sentence        (strict only)
//!     K013 comment not a sentence          (strict only)
//!     K014 comment restates the next line  (strict only)
//!
//! A call is a recursion edge only when it is a bare function name, or a `self.name(..)`
//! call inside a method. An arbitrary `object.name(..)` call cannot be resolved without
//! type inference, and treating it as an edge flags every function whose name happens to
//! match an unrelated method elsewhere.

use std::collections::{BTreeMap, BTreeSet};
use std::path::Path;

use tree_sitter::{Node, Parser};

pub const MAX_LINES: usize = 60;
pub const MAX_DEPTH: usize = 3;
pub const MAX_PARAMS: usize = 4;
pub const MAX_COGNITIVE: usize = 15;
pub const MAX_SHARED: usize = 2;
pub const MIN_RATIO: f64 = 0.8;

const ADD_LEVEL: [&str; 6] = [
    "if_statement",
    "for_statement",
    "while_statement",
    "try_statement",
    "with_statement",
    "elif_clause",
];
const CONTINUE_LEVEL: [&str; 3] = ["else_clause", "except_clause", "finally_clause"];
const PLACEHOLDERS: [&str; 4] = ["TODO", "FIXME", "XXX", "HACK"];
const STOPWORDS: [&str; 28] = [
    "the", "a", "an", "is", "are", "was", "this", "that", "these", "to", "of", "in", "it", "its",
    "and", "or", "for", "with", "be", "by", "on", "at", "from", "as", "we", "you", "if", "so",
];
const MUTABLE: [&str; 6] = [
    "list",
    "dictionary",
    "set",
    "list_comprehension",
    "set_comprehension",
    "dictionary_comprehension",
];

/// One rule violation.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct Finding {
    pub code: String,
    pub line: usize,
    pub message: String,
}

impl Finding {
    fn new(code: &str, line: usize, message: impl Into<String>) -> Self {
        Self {
            code: code.to_string(),
            line,
            message: message.into(),
        }
    }
}

/// A function definition found in the tree.
struct Func<'a> {
    name: String,
    node: Node<'a>,
    receiver: Option<String>,
}

/// Read a source file, falling back to latin-1 for bytes that are not valid UTF-8.
pub fn read_source(path: &Path) -> std::io::Result<String> {
    let bytes = std::fs::read(path)?;
    Ok(match String::from_utf8(bytes.clone()) {
        Ok(text) => text,
        Err(_) => bytes.iter().map(|byte| *byte as char).collect(),
    })
}

fn parser() -> Parser {
    let mut parser = Parser::new();
    parser
        .set_language(&tree_sitter_python::LANGUAGE.into())
        .expect("tree-sitter-python grammar failed to load");
    parser
}

/// Every node beneath root, in document order.
fn walk_all<'a>(root: Node<'a>) -> Vec<Node<'a>> {
    let mut found = Vec::new();
    let mut stack = vec![root];
    while let Some(node) = stack.pop() {
        found.push(node);
        let count = node.child_count();
        for index in (0..count).rev() {
            if let Some(child) = node.child(index) {
                stack.push(child);
            }
        }
    }
    found
}

fn text(node: Node, source: &[u8]) -> String {
    String::from_utf8_lossy(&source[node.byte_range()]).to_string()
}

/// The first error node, if the parse failed.
fn first_error<'a>(root: Node<'a>) -> Option<Node<'a>> {
    let mut stack = vec![root];
    while let Some(node) = stack.pop() {
        if node.is_error() || node.is_missing() {
            return Some(node);
        }
        let count = node.child_count();
        for index in (0..count).rev() {
            if let Some(child) = node.child(index) {
                stack.push(child);
            }
        }
    }
    None
}

fn is_method(node: Node) -> bool {
    let mut parent = node.parent();
    while let Some(current) = parent {
        match current.kind() {
            "class_definition" => return true,
            "function_definition" => return false,
            "module" => return false,
            _ => {}
        }
        parent = current.parent();
    }
    false
}

fn parameters_node(node: Node) -> Option<Node> {
    node.child_by_field_name("parameters")
}

fn first_parameter_name(parameters: Node, source: &[u8]) -> Option<String> {
    let mut cursor = parameters.walk();
    for child in parameters.named_children(&mut cursor) {
        if child.kind() == "comment" {
            continue;
        }
        return Some(text(child, source));
    }
    None
}

fn collect_functions<'a>(root: Node<'a>, source: &[u8]) -> Vec<Func<'a>> {
    let mut found = Vec::new();
    for node in walk_all(root) {
        if node.kind() != "function_definition" {
            continue;
        }
        let name = node
            .child_by_field_name("name")
            .map(|child| text(child, source))
            .unwrap_or_default();
        let method = is_method(node);
        let receiver = parameters_node(node)
            .filter(|_| method)
            .and_then(|params| first_parameter_name(params, source));
        found.push(Func {
            name,
            node,
            receiver,
        });
    }
    found
}

fn arity(node: Node) -> usize {
    let Some(parameters) = parameters_node(node) else {
        return 0;
    };
    let mut cursor = parameters.walk();
    parameters
        .named_children(&mut cursor)
        .filter(|child| child.kind() != "comment")
        .count()
}

/// Call edges, cognitive score and nesting depth, gathered in one traversal.
fn stats(func: &Func, source: &[u8]) -> (BTreeSet<String>, usize, usize) {
    let mut edges = BTreeSet::new();
    let mut cognitive = 0usize;
    let mut deepest = 0usize;
    let mut stack = vec![(func.node, 0usize)];
    while let Some((node, depth)) = stack.pop() {
        deepest = deepest.max(depth);
        if node.kind() == "call" {
            if let Some(target) = node.child_by_field_name("function") {
                record_edge(target, func, source, &mut edges);
            }
        }
        if node.kind() == "boolean_operator" {
            let extra = node.named_child_count().saturating_sub(1);
            cognitive += extra;
        }
        let count = node.child_count();
        for index in (0..count).rev() {
            if let Some(child) = node.child(index) {
                let opens =
                    ADD_LEVEL.contains(&child.kind()) || CONTINUE_LEVEL.contains(&child.kind());
                let step = usize::from(opens);
                if ADD_LEVEL.contains(&child.kind()) {
                    cognitive += 1 + depth;
                }
                stack.push((child, depth + step));
            }
        }
    }
    (edges, cognitive, deepest)
}

fn record_edge(target: Node, func: &Func, source: &[u8], edges: &mut BTreeSet<String>) {
    match target.kind() {
        "identifier" => {
            edges.insert(text(target, source));
        }
        "attribute" => {
            let attribute = target
                .child_by_field_name("attribute")
                .map(|child| text(child, source))
                .unwrap_or_default();
            let object = target
                .child_by_field_name("object")
                .map(|child| text(child, source))
                .unwrap_or_default();
            if attribute == func.name {
                if let Some(receiver) = &func.receiver {
                    if &object == receiver {
                        edges.insert(func.name.clone());
                    }
                }
            }
        }
        _ => {}
    }
}

fn find_recursion(edges: &BTreeMap<String, BTreeSet<String>>) -> BTreeSet<String> {
    let mut recursive = BTreeSet::new();
    for start in edges.keys() {
        let mut seen: BTreeSet<String> = BTreeSet::new();
        let mut pending: Vec<String> = edges[start].iter().cloned().collect();
        while let Some(current) = pending.pop() {
            if &current == start {
                recursive.insert(start.clone());
                break;
            }
            if seen.insert(current.clone()) {
                if let Some(next) = edges.get(&current) {
                    pending.extend(next.iter().cloned());
                }
            }
        }
    }
    recursive
}

fn size_findings(
    name: &str,
    line: usize,
    span: usize,
    depth: usize,
    params: usize,
    cognitive: usize,
) -> Vec<Finding> {
    let mut found = Vec::new();
    if span > MAX_LINES {
        found.push(Finding::new(
            "K002",
            line,
            format!("{name} is {span} lines, limit {MAX_LINES}"),
        ));
    }
    if depth > MAX_DEPTH {
        found.push(Finding::new(
            "K003",
            line,
            format!("{name} nests {depth} deep, limit {MAX_DEPTH}"),
        ));
    }
    if params > MAX_PARAMS {
        found.push(Finding::new(
            "K004",
            line,
            format!("{name} takes {params} parameters, limit {MAX_PARAMS}"),
        ));
    }
    if cognitive > MAX_COGNITIVE {
        found.push(Finding::new(
            "K005",
            line,
            format!("{name} scores {cognitive}, limit {MAX_COGNITIVE}"),
        ));
    }
    found
}

fn swallow_findings(root: Node, source: &[u8]) -> Vec<Finding> {
    let mut found = Vec::new();
    for node in walk_all(root) {
        if node.kind() != "except_clause" {
            continue;
        }
        let mut cursor = node.walk();
        let named: Vec<Node> = node.named_children(&mut cursor).collect();
        let type_node = named.iter().find(|child| child.kind() != "block");
        match type_node {
            None => found.push(Finding::new(
                "K006",
                node.start_position().row + 1,
                "blanket exception swallowed",
            )),
            Some(typed) => {
                if text(*typed, source).trim() == "Exception" {
                    found.push(Finding::new(
                        "K006",
                        node.start_position().row + 1,
                        "blanket exception swallowed",
                    ));
                }
            }
        }
    }
    found
}

fn state_findings(root: Node, source: &[u8]) -> Vec<Finding> {
    let mut found = Vec::new();
    let mut cursor = root.walk();
    for child in root.named_children(&mut cursor) {
        // A module-level statement is wrapped: `CACHE = {}` arrives as
        // expression_statement > assignment, so the wrapper has to be unwrapped.
        let node = if child.kind() == "expression_statement" {
            match child.named_child(0) {
                Some(inner) => inner,
                None => continue,
            }
        } else {
            child
        };
        match node.kind() {
            "augmented_assignment" => {
                if let Some(left) = node.child_by_field_name("left") {
                    if left.kind() == "identifier" {
                        found.push(Finding::new(
                            "K007",
                            node.start_position().row + 1,
                            format!("{} mutated at module scope", text(left, source)),
                        ));
                    }
                }
            }
            "assignment" => {
                let Some(left) = node.child_by_field_name("left") else {
                    continue;
                };
                let Some(right) = node.child_by_field_name("right") else {
                    continue;
                };
                if left.kind() == "subscript" {
                    found.push(Finding::new(
                        "K007",
                        node.start_position().row + 1,
                        "container mutated at module scope",
                    ));
                } else if left.kind() == "identifier" && MUTABLE.contains(&right.kind()) {
                    found.push(Finding::new(
                        "K007",
                        node.start_position().row + 1,
                        format!("{} held at module scope", text(left, source)),
                    ));
                }
            }
            _ => {}
        }
    }
    found
}

fn is_banner(body: &str) -> bool {
    let squeezed: Vec<char> = body.chars().filter(|c| !c.is_whitespace()).collect();
    if squeezed.len() < 6 {
        return false;
    }
    let first = squeezed[0];
    !first.is_alphanumeric() && squeezed.iter().all(|c| *c == first)
}

fn looks_like_code(body: &str) -> bool {
    let lowered = body.to_lowercase();
    for prefix in ["e.g.", "i.e.", "example", "see ", "cf."] {
        if lowered.starts_with(prefix) {
            return false;
        }
    }
    if body.len() <= 3 {
        return false;
    }
    if !body.contains('=') && !body.contains('(') && !body.contains(':') && !body.contains('[') {
        return false;
    }
    let mut parser = parser();
    match parser.parse(body, None) {
        Some(tree) => !tree.root_node().has_error(),
        None => false,
    }
}

fn words(line: &str) -> BTreeSet<String> {
    line.replace(['_', '.', ':'], " ")
        .split(|c: char| !c.is_alphanumeric())
        .filter(|part| !part.is_empty())
        .map(|part| part.to_lowercase())
        .filter(|part| !STOPWORDS.contains(&part.as_str()))
        .collect()
}

fn restates(body: &str, next_line: &str) -> bool {
    let said = words(body);
    let written = words(next_line);
    if said.is_empty() || written.is_empty() {
        return false;
    }
    let shared = said.intersection(&written).count();
    shared >= MAX_SHARED && (shared as f64) / (said.len() as f64) >= MIN_RATIO
}

fn ends_sentence(value: &str) -> bool {
    value.ends_with('.') || value.ends_with('!') || value.ends_with('?')
}

fn comment_findings(source: &str, root: Node, strict: bool) -> Vec<Finding> {
    let lines: Vec<&str> = source.lines().collect();
    let mut found = Vec::new();
    for node in walk_all(root) {
        if node.kind() != "comment" {
            continue;
        }
        let raw = &source[node.byte_range()];
        let row = node.start_position().row;
        if row == 0 && raw.starts_with("#!") {
            continue;
        }
        let body = raw.trim_start_matches('#').trim();
        if body.is_empty() {
            continue;
        }
        let mut line_findings = Vec::new();
        if PLACEHOLDERS.iter().any(|marker| body.contains(marker)) {
            line_findings.push(Finding::new("K008", row + 1, body.to_string()));
        } else if is_banner(body) {
            line_findings.push(Finding::new("K010", row + 1, body.to_string()));
        } else if looks_like_code(body) {
            line_findings.push(Finding::new("K009", row + 1, body.to_string()));
        }
        if strict && line_findings.is_empty() {
            if !ends_sentence(body) {
                line_findings.push(Finding::new("K013", row + 1, body.to_string()));
            }
            let next = lines.get(row + 1).copied().unwrap_or("");
            if restates(body, next) {
                line_findings.push(Finding::new("K014", row + 1, body.to_string()));
            }
        }
        found.extend(line_findings);
    }
    found
}

fn string_body(node: Node, source: &[u8]) -> Option<String> {
    let raw = text(node, source);
    let trimmed = raw.trim();
    let without_prefix: String = trimmed
        .chars()
        .skip_while(|c| c.is_alphabetic() && !c.is_whitespace())
        .collect();
    for quote in ["\"\"\"", "'''"] {
        if without_prefix.starts_with(quote)
            && without_prefix.ends_with(quote)
            && without_prefix.len() >= 6
        {
            return Some(without_prefix[3..without_prefix.len() - 3].to_string());
        }
    }
    for quote in ['"', '\''] {
        if without_prefix.starts_with(quote)
            && without_prefix.ends_with(quote)
            && without_prefix.len() >= 2
        {
            return Some(without_prefix[1..without_prefix.len() - 1].to_string());
        }
    }
    None
}

fn docstring_of(container: Node, source: &[u8]) -> Option<String> {
    let body = if container.kind() == "function_definition" {
        container.child_by_field_name("body")?
    } else {
        container
    };
    let mut cursor = body.walk();
    let first = body.named_children(&mut cursor).next()?;
    if first.kind() != "expression_statement" {
        return None;
    }
    let mut inner = first.walk();
    let string = first.named_children(&mut inner).next()?;
    if string.kind() != "string" {
        return None;
    }
    string_body(string, source)
}

fn docstring_findings(root: Node, source: &[u8], strict: bool) -> Vec<Finding> {
    let mut found = Vec::new();
    if docstring_of(root, source).is_none() {
        found.push(Finding::new("K011", 1, "module has no docstring"));
    }
    let mut cursor = root.walk();
    for node in root.named_children(&mut cursor) {
        if node.kind() != "function_definition" {
            continue;
        }
        let Some(name) = node
            .child_by_field_name("name")
            .map(|child| text(child, source))
        else {
            continue;
        };
        match docstring_of(node, source) {
            None => {
                if !name.starts_with('_') {
                    found.push(Finding::new(
                        "K011",
                        node.start_position().row + 1,
                        format!("{name} is undocumented"),
                    ));
                }
            }
            Some(documented) => {
                if strict {
                    let first_line = documented.lines().next().unwrap_or("").trim();
                    if !ends_sentence(first_line) {
                        found.push(Finding::new(
                            "K012",
                            node.start_position().row + 1,
                            format!("{name} summary is not a sentence"),
                        ));
                    }
                }
            }
        }
    }
    found
}

/// Every finding for one source file.
pub fn check_source(source: &str, strict: bool) -> Vec<Finding> {
    let mut parser = parser();
    let Some(tree) = parser.parse(source, None) else {
        return vec![Finding::new(
            "K000",
            0,
            "cannot parse: parser returned no tree",
        )];
    };
    let root = tree.root_node();
    if let Some(error) = first_error(root) {
        let line = error.start_position().row + 1;
        return vec![Finding::new("K000", line, "cannot parse: syntax error")];
    }
    let bytes = source.as_bytes();
    let mut found = Vec::new();
    let functions = collect_functions(root, bytes);
    let mut edges: BTreeMap<String, BTreeSet<String>> = BTreeMap::new();
    for func in &functions {
        let (targets, cognitive, depth) = stats(func, bytes);
        edges.entry(func.name.clone()).or_default().extend(targets);
        let span = func.node.end_position().row - func.node.start_position().row + 1;
        found.extend(size_findings(
            &func.name,
            func.node.start_position().row + 1,
            span,
            depth,
            arity(func.node),
            cognitive,
        ));
    }
    for name in find_recursion(&edges) {
        for func in functions.iter().filter(|func| func.name == name) {
            found.push(Finding::new(
                "K001",
                func.node.start_position().row + 1,
                format!("{name} recurses"),
            ));
        }
    }
    found.extend(swallow_findings(root, bytes));
    found.extend(state_findings(root, bytes));
    found.extend(docstring_findings(root, bytes, strict));
    found.extend(comment_findings(source, root, strict));
    found.sort();
    found
}

/// Every finding for one file on disk.
pub fn check_file(path: &Path, strict: bool) -> std::io::Result<Vec<Finding>> {
    let source = read_source(path)?;
    Ok(check_source(&source, strict))
}
