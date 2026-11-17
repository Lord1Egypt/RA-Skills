//! The regression corpus: every fixture must produce exactly its expected code set.
//!
//! A case passes only when the reported set equals the expected set, so a false
//! positive fails just as a miss does. These are the same 26 cases the Python suite
//! asserted, which is what makes the port verifiable rather than merely plausible.

use std::collections::BTreeSet;
use std::path::{Path, PathBuf};

use kroko::check_file;

struct Case {
    fixture: &'static str,
    strict: bool,
    expected: &'static [&'static str],
}

const CASES: &[Case] = &[
    Case {
        fixture: "good_clean.py",
        strict: false,
        expected: &[],
    },
    Case {
        fixture: "good_clean.py",
        strict: true,
        expected: &[],
    },
    Case {
        fixture: "bad_recursion.py",
        strict: false,
        expected: &["K001"],
    },
    Case {
        fixture: "bad_mutual.py",
        strict: false,
        expected: &["K001"],
    },
    Case {
        fixture: "bad_long.py",
        strict: false,
        expected: &["K002"],
    },
    Case {
        fixture: "bad_nesting.py",
        strict: false,
        expected: &["K003"],
    },
    Case {
        fixture: "bad_params.py",
        strict: false,
        expected: &["K004"],
    },
    Case {
        fixture: "bad_params_posonly.py",
        strict: false,
        expected: &["K004"],
    },
    Case {
        fixture: "bad_cognitive.py",
        strict: false,
        expected: &["K005"],
    },
    Case {
        fixture: "bad_swallow.py",
        strict: false,
        expected: &["K006"],
    },
    Case {
        fixture: "bad_state.py",
        strict: false,
        expected: &["K007"],
    },
    Case {
        fixture: "bad_state_items.py",
        strict: false,
        expected: &["K007"],
    },
    Case {
        fixture: "bad_todo.py",
        strict: false,
        expected: &["K008"],
    },
    Case {
        fixture: "bad_commented_code.py",
        strict: false,
        expected: &["K009"],
    },
    Case {
        fixture: "bad_banner.py",
        strict: false,
        expected: &["K010"],
    },
    Case {
        fixture: "bad_nodoc.py",
        strict: false,
        expected: &["K011"],
    },
    Case {
        fixture: "bad_sentence.py",
        strict: false,
        expected: &[],
    },
    Case {
        fixture: "bad_sentence.py",
        strict: true,
        expected: &["K012", "K013"],
    },
    Case {
        fixture: "bad_restate.py",
        strict: false,
        expected: &[],
    },
    Case {
        fixture: "bad_restate.py",
        strict: true,
        expected: &["K014"],
    },
    Case {
        fixture: "bad_restate_short.py",
        strict: true,
        expected: &["K014"],
    },
    Case {
        fixture: "bad_method_recursion.py",
        strict: false,
        expected: &["K001"],
    },
    Case {
        fixture: "good_method_calls.py",
        strict: false,
        expected: &[],
    },
    Case {
        fixture: "bad_unparseable.py",
        strict: false,
        expected: &["K000"],
    },
    Case {
        fixture: "bad_latin1.py",
        strict: false,
        expected: &[],
    },
    Case {
        fixture: "bad_latin1.py",
        strict: true,
        expected: &[],
    },
];

fn fixture_dir() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .expect("crate lives inside the repository")
        .join("tests")
        .join("fixtures")
}

fn codes(path: &Path, strict: bool) -> BTreeSet<String> {
    check_file(path, strict)
        .expect("fixture should be readable")
        .into_iter()
        .map(|finding| finding.code)
        .collect()
}

#[test]
fn every_fixture_produces_exactly_its_expected_codes() {
    let directory = fixture_dir();
    let mut failures = Vec::new();
    for case in CASES {
        let path = directory.join(case.fixture);
        let actual = codes(&path, case.strict);
        let expected: BTreeSet<String> =
            case.expected.iter().map(|code| code.to_string()).collect();
        if actual != expected {
            failures.push(format!(
                "{} strict={}: expected {:?}, got {:?}",
                case.fixture, case.strict, expected, actual
            ));
        }
    }
    assert!(
        failures.is_empty(),
        "{} of {} cases failed:\n{}",
        failures.len(),
        CASES.len(),
        failures.join("\n")
    );
}
