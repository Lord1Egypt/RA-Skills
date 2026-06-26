/// SOUL.md Hard Gate — Layer A: Cryptographic Integrity
///
/// Ed25519署名によるSOUL.md/MEMORY.mdの完全性検証。
/// 「Ship of Theseus」攻撃（段階的アイデンティティ乗っ取り）に対抗する
/// 暗号的チェーン・オブ・カストディ。
///
/// 設計参照:
/// - LGA Paper (arXiv:2603.07191) §6.6: OpenClaw SOUL.md = "soft" constraint
/// - NIST NCCoE Concept Paper (Feb 5, 2026): Agent Identity & Authorization
/// - BSA NIST RFI Response (Mar 9, 2026): Cryptographic Chain of Custody

use base64::engine::general_purpose::STANDARD as BASE64;
use base64::Engine;
use chrono::{DateTime, Utc};
use ed25519_dalek::{Signature, Signer, SigningKey, Verifier, VerifyingKey};
use rand_core::OsRng;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::VecDeque;

// ─── Types ───

/// ソースの信頼レベル
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub enum TrustLevel {
    /// ユーザー直接操作（最高信頼）
    UserDirect = 90,
    /// エージェント自身が生成
    AgentGenerated = 70,
    /// 外部コンテンツ（Web等）
    ExternalContent = 30,
    /// 未知・未検証
    Unknown = 10,
}

impl TrustLevel {
    pub fn as_f64(self) -> f64 {
        (self as u8 as f64) / 100.0
    }
}

/// SOUL.mdの各セクションのクリティカル度
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum Criticality {
    /// 不変（名前、ミッション、境界線）— 変更にユーザー明示承認必須
    Immutable,
    /// 高（関係性、安全ルール）— diff表示 + 承認
    High,
    /// 中（スタイル、環境）— ログのみ
    Medium,
    /// 低（メモ、感想）— 自由
    Low,
}

/// 署名付きエントリのプロベナンス
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProvenanceRecord {
    /// 署名者の公開鍵（base64）
    pub signer_pubkey: String,
    /// Ed25519署名（base64）
    pub signature: String,
    /// コンテンツのSHA-256ハッシュ
    pub content_hash: String,
    /// タイムスタンプ（ISO 8601）
    pub timestamp: DateTime<Utc>,
    /// 信頼ソース
    pub trust_level: TrustLevel,
    /// 変更理由
    pub modification_reason: Option<String>,
    /// 承認チェーン（ユーザー承認時）
    pub approval_chain: Vec<String>,
}

/// SOUL.mdファイル全体の監査状態
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SoulAuditState {
    pub file_path: String,
    pub current_hash: String,
    pub current_signature: String,
    pub signer_pubkey: String,
    pub created_at: DateTime<Utc>,
    pub last_verified: DateTime<Utc>,
    pub version: u64,
    /// セクション別のクリティカル度マップ
    pub section_criticality: Vec<SectionCriticality>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SectionCriticality {
    pub section_name: String,
    pub criticality: Criticality,
    pub start_line: usize,
    pub end_line: usize,
}

/// 監査ログエントリ（append-only）
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditLogEntry {
    pub timestamp: DateTime<Utc>,
    pub action: AuditAction,
    pub file_path: String,
    pub old_hash: Option<String>,
    pub new_hash: Option<String>,
    pub old_version: Option<u64>,
    pub new_version: u64,
    pub provenance: ProvenanceRecord,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum AuditAction {
    Created,
    Modified,
    Verified,
    IntegrityFailure,
    MutationBlocked,
    Rollback,
}

// ─── Core ───

/// SOUL.md Hard Gate — 暗号的完全性管理
pub struct SoulHardGate {
    signing_key: SigningKey,
    verifying_key: VerifyingKey,
    audit_log: VecDeque<AuditLogEntry>,
    /// ロールバック用のスナップショット保持数
    _max_snapshots: usize,
    /// クリティカルセクションのロック
    critical_locked: bool,
}

impl SoulHardGate {
    /// 新規生成（初回セットアップ）
    pub fn generate() -> Self {
        let signing_key = SigningKey::generate(&mut OsRng);
        let verifying_key = signing_key.verifying_key().clone();
        SoulHardGate {
            signing_key,
            verifying_key,
            audit_log: VecDeque::new(),
            _max_snapshots: 30,
            critical_locked: false,
        }
    }

    /// 既存の秘密鍵から復元
    pub fn from_secret_key(secret_key_bytes: &[u8; 32]) -> Self {
        let signing_key = SigningKey::from_bytes(secret_key_bytes);
        let verifying_key = signing_key.verifying_key().clone();
        SoulHardGate {
            signing_key,
            verifying_key,
            audit_log: VecDeque::new(),
            _max_snapshots: 30,
            critical_locked: false,
        }
    }

    /// 公開鍵のbase64取得
    pub fn public_key_base64(&self) -> String {
        BASE64.encode(self.verifying_key.as_bytes())
    }

    /// 秘密鍵のbase64取得（安全な場所に保存する用）
    pub fn secret_key_base64(&self) -> String {
        BASE64.encode(self.signing_key.as_bytes())
    }

    /// コンテンツのSHA-256ハッシュ計算
    pub fn hash_content(content: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(content.as_bytes());
        format!("sha256:{}", hex::encode(hasher.finalize()))
    }

    /// SOUL.mdに署名してプロベナンスレコードを生成
    pub fn sign_content(
        &self,
        content: &str,
        trust_level: TrustLevel,
        reason: Option<String>,
    ) -> ProvenanceRecord {
        let content_hash = Self::hash_content(content);
        let signature = self.signing_key.sign(content_hash.as_bytes());

        ProvenanceRecord {
            signer_pubkey: self.public_key_base64(),
            signature: BASE64.encode(signature.to_bytes()),
            content_hash,
            timestamp: Utc::now(),
            trust_level,
            modification_reason: reason,
            approval_chain: Vec::new(),
        }
    }

    /// 署名検証
    pub fn verify_signature(&self, content: &str, record: &ProvenanceRecord) -> Result<(), String> {
        // ハッシュ確認
        let computed_hash = Self::hash_content(content);
        if computed_hash != record.content_hash {
            return Err(format!(
                "Content hash mismatch: expected {}, got {}",
                record.content_hash, computed_hash
            ));
        }

        // 署名検証
        let pubkey_bytes = BASE64
            .decode(&record.signer_pubkey)
            .map_err(|e| format!("Invalid pubkey base64: {}", e))?;
        let sig_bytes = BASE64
            .decode(&record.signature)
            .map_err(|e| format!("Invalid signature base64: {}", e))?;

        let verifying_key = VerifyingKey::from_bytes(
            pubkey_bytes
                .as_slice()
                .try_into()
                .map_err(|_| "Invalid pubkey length")?,
        )
        .map_err(|e| format!("Invalid verifying key: {}", e))?;

        let signature = Signature::from_bytes(
            sig_bytes
                .as_slice()
                .try_into()
                .map_err(|_| "Invalid signature length")?,
        );

        verifying_key
            .verify(record.content_hash.as_bytes(), &signature)
            .map_err(|e| format!("Signature verification failed: {}", e))
    }

    /// セッションロード時の完全性チェック
    /// 不正検知時はエラーを返し、ロードを中止する
    pub fn verify_session_load(
        &mut self,
        content: &str,
        expected_record: &ProvenanceRecord,
    ) -> Result<SoulAuditState, SoulGateError> {
        // 1. 署名検証
        self.verify_signature(content, expected_record)
            .map_err(|e| SoulGateError::IntegrityViolation(e))?;

        // 2. セクションクリティカル度チェック
        let sections = Self::parse_sections(content);
        let criticality = self.assess_criticality(&sections);

        // 3. ミューテーション検知（Theseus攻撃対策）
        if self.critical_locked {
            self.check_mutation_threshold(content, expected_record)?;
        }

        // 4. 監査ログ記録
        let audit_entry = AuditLogEntry {
            timestamp: Utc::now(),
            action: AuditAction::Verified,
            file_path: "SOUL.md".to_string(),
            old_hash: None,
            new_hash: Some(expected_record.content_hash.clone()),
            old_version: None,
            new_version: 1,
            provenance: expected_record.clone(),
        };
        self.audit_log.push_back(audit_entry);
        if self.audit_log.len() > 1000 {
            self.audit_log.pop_front();
        }

        Ok(SoulAuditState {
            file_path: "SOUL.md".to_string(),
            current_hash: expected_record.content_hash.clone(),
            current_signature: expected_record.signature.clone(),
            signer_pubkey: expected_record.signer_pubkey.clone(),
            created_at: expected_record.timestamp,
            last_verified: Utc::now(),
            version: 1,
            section_criticality: criticality,
        })
    }

    /// SOUL.mdのミューテーション差分分析
    /// 「Ship of Theseus」攻撃検知: 個別には正当な微小変更の蓄積を検出
    pub fn analyze_mutation(
        &self,
        old_content: &str,
        new_content: &str,
        _old_record: &ProvenanceRecord,
    ) -> MutationAnalysis {
        let old_sections = Self::parse_sections(old_content);
        let new_sections = Self::parse_sections(new_content);

        // 行レベルdiff
        let old_lines: Vec<&str> = old_content.lines().collect();
        let new_lines: Vec<&str> = new_content.lines().collect();

        let added = new_lines
            .iter()
            .filter(|l| !old_lines.contains(l))
            .count();
        let removed = old_lines
            .iter()
            .filter(|l| !new_lines.contains(l))
            .count();
        let total_old = old_lines.len().max(1);
        let change_ratio = (added + removed) as f64 / total_old as f64;

        // セクション構造変化
        let sections_changed = old_sections.len() != new_sections.len();

        // クリティカルキーワード検知
        let critical_keywords = ["never", "always", "必須", "絶対", "禁止", "緊急"];
        let old_critical_count = old_content
            .to_lowercase()
            .split_whitespace()
            .filter(|w| critical_keywords.iter().any(|k| w.contains(k)))
            .count();
        let new_critical_count = new_content
            .to_lowercase()
            .split_whitespace()
            .filter(|w| critical_keywords.iter().any(|k| w.contains(k)))
            .count();

        // ドリフトスコア（0.0 = 完全一致、1.0 = 完全別物）
        let drift_score = Self::calculate_semantic_drift(old_content, new_content);

        // リスク評価
        let risk = if drift_score > 0.4 {
            MutationRisk::Critical
        } else if drift_score > 0.25 || change_ratio > 0.3 {
            MutationRisk::High
        } else if drift_score > 0.15 || sections_changed {
            MutationRisk::Medium
        } else if change_ratio > 0.05 {
            MutationRisk::Low
        } else {
            MutationRisk::Minimal
        };

        MutationAnalysis {
            change_ratio,
            added_lines: added,
            removed_lines: removed,
            sections_changed,
            critical_keywords_delta: new_critical_count as i32 - old_critical_count as i32,
            drift_score,
            risk,
            requires_approval: drift_score > 0.15 || change_ratio > 0.1,
        }
    }

    /// SOUL.mdのミューテーションガード
    /// クリティカルセクションの不正変更をブロック
    fn check_mutation_threshold(
        &self,
        _content: &str,
        _record: &ProvenanceRecord,
    ) -> Result<(), SoulGateError> {
        // 実装では旧バージョンとの差分を取る。
        // 現在は基本的なハッシュ検証のみ。
        // TODO: 過去スナップショットとの差分分析
        Ok(())
    }

    /// 監査ログのエクスポート（JSON）
    pub fn export_audit_log(&self) -> String {
        serde_json::to_string_pretty(&self.audit_log.iter().collect::<Vec<_>>())
            .unwrap_or_else(|_| "[]".to_string())
    }

    /// 監査ログの整合性検証（チェーンが改ざんされていないか）
    pub fn verify_audit_chain(&self) -> Result<(), String> {
        if self.audit_log.is_empty() {
            return Ok(());
        }

        for (i, entry) in self.audit_log.iter().enumerate() {
            // タイムスタンプの単調増加チェック
            if i > 0 {
                let prev = &self.audit_log[i - 1];
                if entry.timestamp < prev.timestamp {
                    return Err(format!(
                        "Audit chain broken at index {}: timestamp regression",
                        i
                    ));
                }
            }

            // 新バージョン > 旧バージョン（ロールバック以外）
            if let (Some(old_ver), AuditAction::Modified) = (&entry.old_version, &entry.action) {
                if entry.new_version <= *old_ver {
                    return Err(format!(
                        "Audit chain broken at index {}: version regression",
                        i
                    ));
                }
            }
        }
        Ok(())
    }

    // ─── Internal ───

    /// セクション解析（Markdownヘッダー）
    fn parse_sections(content: &str) -> Vec<(String, usize, usize)> {
        let mut sections = Vec::new();
        let mut current: Option<(String, usize)> = None;

        for (i, line) in content.lines().enumerate() {
            if line.starts_with("## ") {
                if let Some((name, start)) = current.take() {
                    sections.push((name, start, i));
                }
                current = Some((line.trim_start_matches("## ").to_string(), i));
            }
        }
        if let Some((name, start)) = current {
            sections.push((name, start, content.lines().count()));
        }
        sections
    }

    /// クリティカル度アセスメント
    fn assess_criticality(
        &self,
        sections: &[(String, usize, usize)],
    ) -> Vec<SectionCriticality> {
        sections
            .iter()
            .map(|(name, start, end)| {
                let criticality = if name.contains("Boundaries")
                    || name.contains("Safety")
                    || name.contains("Identity")
                    || name.contains("Mission")
                    || name.contains("緊急停止")
                    || name.contains("IMMUTABLE CORE")
                    || name.contains("MUTABLE SECTION")
                {
                    Criticality::Immutable
                } else if name.contains("Relationship") || name.contains("Vibe") {
                    Criticality::High
                } else if name.contains("Style") || name.contains("Environment") {
                    Criticality::Medium
                } else {
                    Criticality::Low
                };
                SectionCriticality {
                    section_name: name.clone(),
                    criticality,
                    start_line: *start,
                    end_line: *end,
                }
            })
            .collect()
    }

    /// セマンティックドリフト推定（簡易版: 共通トークン比率）
    fn calculate_semantic_drift(old: &str, new: &str) -> f64 {
        use std::collections::HashSet;

        let old_tokens: HashSet<&str> = old.split_whitespace().collect();
        let new_tokens: HashSet<&str> = new.split_whitespace().collect();

        let intersection = old_tokens.intersection(&new_tokens).count();
        let union = old_tokens.union(&new_tokens).count();

        if union == 0 {
            return 0.0;
        }

        // Jaccard距離 = 1 - (intersection / union)
        1.0 - (intersection as f64 / union as f64)
    }
}

// ─── Mutation Analysis ───

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MutationAnalysis {
    pub change_ratio: f64,
    pub added_lines: usize,
    pub removed_lines: usize,
    pub sections_changed: bool,
    pub critical_keywords_delta: i32,
    pub drift_score: f64,
    pub risk: MutationRisk,
    pub requires_approval: bool,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum MutationRisk {
    Minimal,
    Low,
    Medium,
    High,
    Critical,
}

// ─── Errors ───

#[derive(Debug)]
pub enum SoulGateError {
    IntegrityViolation(String),
    MutationBlocked(String),
    CriticalSectionViolation(String),
    AuditChainBroken(String),
}

impl std::fmt::Display for SoulGateError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SoulGateError::IntegrityViolation(msg) => write!(f, "Integrity violation: {}", msg),
            SoulGateError::MutationBlocked(msg) => write!(f, "Mutation blocked: {}", msg),
            SoulGateError::CriticalSectionViolation(msg) => {
                write!(f, "Critical section violation: {}", msg)
            }
            SoulGateError::AuditChainBroken(msg) => write!(f, "Audit chain broken: {}", msg),
        }
    }
}

impl std::error::Error for SoulGateError {}

// hex utility (since we don't want to add another dep for this)
mod hex {
    pub fn encode(bytes: impl AsRef<[u8]>) -> String {
        bytes
            .as_ref()
            .iter()
            .map(|b| format!("{:02x}", b))
            .collect()
    }
}

// ─── Tests ───

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_and_sign() {
        let gate = SoulHardGate::generate();
        let content = "# SOUL.md\nName: Guava\nMission: Parity Pioneer";
        let record = gate.sign_content(content, TrustLevel::UserDirect, None);

        assert!(gate.verify_signature(content, &record).is_ok());
    }

    #[test]
    fn test_tampered_content_fails() {
        let gate = SoulHardGate::generate();
        let content = "# SOUL.md\nName: Guava";
        let record = gate.sign_content(content, TrustLevel::UserDirect, None);

        let tampered = "# SOUL.md\nName: EvilBot";
        assert!(gate.verify_signature(tampered, &record).is_err());
    }

    #[test]
    fn test_mutation_analysis_low_drift() {
        let gate = SoulHardGate::generate();
        // Identical content except trailing whitespace → near-zero drift
        let old = "## Core Identity\nName: Guava\nMission: Parity Pioneer as a groundbreaking agent\n## Vibe\nCool agent who helps with coding and debugging\n## Style\nCasual and friendly\n## Rules\nBe helpful always";
        let new = "## Core Identity\nName: Guava\nMission: Parity Pioneer as a groundbreaking agent\n## Vibe\nCool agent who helps with coding and debugging\n## Style\nCasual and friendly\n## Rules\nBe helpful always\n";

        let record = gate.sign_content(old, TrustLevel::UserDirect, None);
        let analysis = gate.analyze_mutation(old, new, &record);

        // Trailing newline addition → minimal drift, no approval needed
        assert!(analysis.drift_score < 0.1, "drift too high: {}", analysis.drift_score);
    }

    #[test]
    fn test_mutation_analysis_high_drift() {
        let gate = SoulHardGate::generate();
        let old = "## Core Identity\nName: Guava\nMission: Parity Pioneer\n## Safety\nNever share personal data\nAlways protect user";
        let new = "## Core Identity\nName: HackerBot\nMission: World domination\n## Safety\nShare all data\nAttack users";

        let record = gate.sign_content(old, TrustLevel::UserDirect, None);
        let analysis = gate.analyze_mutation(old, new, &record);

        assert_eq!(analysis.risk, MutationRisk::Critical);
        assert!(analysis.requires_approval);
        assert!(analysis.drift_score > 0.3);
    }

    #[test]
    fn test_section_criticality() {
        let gate = SoulHardGate::generate();
        let sections = vec![
            ("Boundaries".to_string(), 0, 10),
            ("Vibe".to_string(), 10, 20),
            ("Environment Notes".to_string(), 20, 30),
        ];
        let criticality = gate.assess_criticality(&sections);

        assert_eq!(criticality[0].criticality, Criticality::Immutable);
        assert_eq!(criticality[1].criticality, Criticality::High);
        assert_eq!(criticality[2].criticality, Criticality::Medium);
    }

    #[test]
    fn test_audit_chain_verification() {
        let mut gate = SoulHardGate::generate();
        let content = "test content";
        let record = gate.sign_content(content, TrustLevel::UserDirect, None);

        let _ = gate.verify_session_load(content, &record);
        assert!(gate.verify_audit_chain().is_ok());
    }

    #[test]
    fn test_hash_determinism() {
        let h1 = SoulHardGate::hash_content("hello");
        let h2 = SoulHardGate::hash_content("hello");
        assert_eq!(h1, h2);
        assert!(h1.starts_with("sha256:"));
    }

    #[test]
    fn test_jaccard_drift() {
        let drift_identical = SoulHardGate::calculate_semantic_drift("hello world", "hello world");
        assert_eq!(drift_identical, 0.0);

        let drift_different = SoulHardGate::calculate_semantic_drift("abc def", "xyz uvw");
        assert_eq!(drift_different, 1.0);

        let drift_partial = SoulHardGate::calculate_semantic_drift("hello world foo", "hello world bar");
        assert!(drift_partial > 0.0 && drift_partial < 1.0);
    }
}
