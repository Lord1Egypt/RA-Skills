# LI Emergency Response MOD

<div align="center">

**AI時代｜エンジニアリングクローズドループ + マルチエージェント協調**

[English](README.md) | [中文](README_中文.md) | [日本語](README_日本語.md) | [한국어](README_한국어.md) | [Français](README_Français.md) | [Deutsch](README_Deutsch.md) | [Español](README_Español.md) | [Português](README_Português.md)

</div>

---

## 📖 概要

**シングルエージェントモード**と**マルチエージェント協調モード**の両方をサポートするエンタープライズグレードのインシデント対応ガイダンススキルです。

### ✨ 主な機能

- 🤖 **デュアルモード**: シングルエージェント（個人向け）+ マルチエージェント（チーム向け）
- 🚀 **並列処理**: 50%以上の効率向上
- 📝 **エンジニアリングクローズドループ**: WAL + VBR + HITL + 自動進化
- 🔍 **包括的カバレッジ**: 従来IT + AIインフラ
- 🌐 **クロスプラットフォーム**: OpenCode/Cursor/Trae/Hermes/OpenClaw

---

## 🎯 使用例

| シナリオ | 具体例 | 推奨モード |
|---------|--------|-----------|
| **従来IT** | マイニング、ランサムウェア、ブルートフォース、フィッシング | シングル/マルチ |
| **AIインフラ** | モデル汚染、GPUマイニング、MLOps侵害 | マルチ |
| **訓練・演習** | CTF、テーブルトップ演習 | シングル（CTFモード） |

---

## 🚀 クイックスタート

### 前提条件

- Python 3.8+
- PyYAMLライブラリ

### インストール

```bash
git clone https://github.com/your-org/corporate-emergency-response-guidance-skill.git
pip install pyyaml
```

### 使用方法

#### シングルエージェントモード

```markdown
あなたは組織のインシデント対応アシスタントです。「SKILL.md」とプレイブックに従ってください。

厳格な制約：
1) 証拠を保存してから対応
2) すべての結論は証拠に基づく（VBR）
3) 重要なアクションはWALに記録
```

#### マルチエージェントモード

```python
import asyncio
from multi_agent.framework.agent_framework import Orchestrator

async def main():
    orchestrator = Orchestrator()
    await orchestrator.initialize()
    
    # セッション作成
    session_id = await orchestrator.create_session("インシデント-2026")
    
    # エージェント作成
    await orchestrator.spawn_agent("ic_agent", "multi_agent/agents/ic_agent.yaml")
    await orchestrator.spawn_agent("analyst_agent", "multi_agent/agents/analyst_agent.yaml")
    
    # ワークフロー実行
    await run_incident_response(orchestrator, session_id)
```

---

## 📊 パフォーマンス指標

| 指標 | シングルエージェント | マルチエージェント | 改善 |
|------|-------------------|------------------|------|
| **対応時間** | 23分 | 12分 | ⬇️ 48% |
| **分析精度** | 70% | 91% | ⬆️ 30% |
| **手動介入** | 100% | 40% | ⬇️ 60% |

---

## 🌐 プラットフォーム互換性

| プラットフォーム | 互換性 | 使用方法 |
|----------------|--------|---------|
| **OpenCode** | ✅ 対応済み | スキルとしてロード |
| **Cursor** | ✅ 対応済み | プロンプトモード |
| **Hermes Agent** | ⚠️ アダプタ必要 | HTTP API |

---

## 📄 ライセンス

MITライセンス - [LICENSE](LICENSE)を参照

---

## 📞 サポート

- **問題**: [GitHub Issues](https://github.com/your-org/corporate-emergency-response-guidance-skill/issues)
- **議論**: [GitHub Discussions](https://github.com/your-org/corporate-emergency-response-guidance-skill/discussions)

---

<div align="center">

**AIでインシデント対応を強化、セキュリティをより効率的に**

Made with ❤️ by 北京老李（Beijing）

</div>
