/// guard-scan-core — Agentic Security Scanner Core Engine
///
/// v16 Architecture (P0 Implementation):
/// - Layer 0: Memory Integrity Module (MINJA/Zombie Agent defense)
/// - Layer A-D: SOUL.md Hard Gate (Cryptographic Integrity + Mutation Guard)
/// - Existing: Static signature detection (patterns.ts bridge)

pub mod soul_hard_gate;
pub mod memory_integrity;

use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct Finding {
    pub severity: String,
    pub confidence: f64,
    pub category: String,
}

pub fn calculate_risk(findings: &[Finding]) -> u32 {
    if findings.is_empty() {
        return 0;
    }

    let mut score = 0.0;
    let mut has_credential = false;
    let mut has_exfil = false;

    for finding in findings {
        let weight = match finding.severity.as_str() {
            "CRITICAL" => 40.0,
            "HIGH" => 15.0,
            "MEDIUM" => 5.0,
            _ => 2.0,
        };
        score += weight * finding.confidence;
        if finding.category == "credential-handling" {
            has_credential = true;
        }
        if finding.category == "exfiltration" {
            has_exfil = true;
        }
    }

    if has_credential && has_exfil {
        score *= 2.2;
        score *= 1.2;
    }

    score.round().min(100.0) as u32
}

#[cfg(test)]
mod tests {
    use super::{calculate_risk, Finding};

    #[test]
    fn empty_findings_are_zero() {
        assert_eq!(calculate_risk(&[]), 0);
    }

    #[test]
    fn single_critical_matches_ts_contract() {
        let findings = vec![Finding {
            severity: "CRITICAL".into(),
            confidence: 0.95,
            category: "prompt-injection".into(),
        }];
        assert_eq!(calculate_risk(&findings), 38);
    }

    #[test]
    fn credential_exfil_chain_amplifies() {
        let findings = vec![
            Finding {
                severity: "HIGH".into(),
                confidence: 0.82,
                category: "credential-handling".into(),
            },
            Finding {
                severity: "HIGH".into(),
                confidence: 0.82,
                category: "exfiltration".into(),
            },
        ];
        assert_eq!(calculate_risk(&findings), 65);
    }
}
