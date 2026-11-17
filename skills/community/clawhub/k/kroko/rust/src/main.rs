use std::path::{Path, PathBuf};
use std::process::ExitCode;

use kroko::Finding;

fn report(path: &Path, findings: &[Finding]) {
    let verdict = if findings.is_empty() { "PASS" } else { "FAIL" };
    println!(
        "{verdict}  {}  ({} findings)",
        path.display(),
        findings.len()
    );
    for finding in findings {
        println!(
            "        {} line {}: {}",
            finding.code, finding.line, finding.message
        );
    }
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let strict = args.iter().any(|arg| arg == "--strict-comments");
    let paths: Vec<PathBuf> = args
        .iter()
        .filter(|arg| !arg.starts_with("--"))
        .map(PathBuf::from)
        .collect();

    if paths.is_empty() {
        eprintln!("usage: kroko [--strict-comments] FILE [FILE ...]");
        return ExitCode::from(2);
    }

    let mut failing = 0usize;
    for path in &paths {
        match kroko::check_file(path, strict) {
            Ok(findings) => {
                if !findings.is_empty() {
                    failing += 1;
                }
                report(path, &findings);
            }
            Err(error) => {
                let unreadable = vec![Finding {
                    code: "K000".to_string(),
                    line: 0,
                    message: format!("cannot read: {error}"),
                }];
                failing += 1;
                report(path, &unreadable);
            }
        }
    }

    println!(
        "\n{} file(s), {} failing, strict={strict}",
        paths.len(),
        failing
    );
    if failing > 0 {
        ExitCode::from(1)
    } else {
        ExitCode::SUCCESS
    }
}
