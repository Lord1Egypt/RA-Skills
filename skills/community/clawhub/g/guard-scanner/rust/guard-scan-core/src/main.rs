use std::io::{self, Read};

use serde::{Deserialize, Serialize};

use guard_scan_core::{calculate_risk, Finding};

#[derive(Debug, Deserialize)]
struct Fixture {
    name: String,
    expected: u32,
    findings: Vec<Finding>,
}

#[derive(Debug, Serialize)]
struct FixtureResult {
    name: String,
    expected: u32,
    actual: u32,
}

#[derive(Debug, Serialize)]
struct Output {
    results: Vec<FixtureResult>,
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let fixtures: Vec<Fixture> = serde_json::from_str(&input).unwrap();

    let results = fixtures
        .into_iter()
        .map(|fixture| FixtureResult {
            name: fixture.name,
            expected: fixture.expected,
            actual: calculate_risk(&fixture.findings),
        })
        .collect::<Vec<_>>();

    println!("{}", serde_json::to_string(&Output { results }).unwrap());
}
