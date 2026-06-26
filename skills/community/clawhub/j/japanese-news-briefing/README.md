# Japanese News Briefing 🖤

**1 日 4 回の自動ニュースブリーフィングを日本語で配信**

---

## 🎯 何ができる？

このスキルは OpenClaw エージェントが自動的に 1 日 4 回ニュースを収集し、日本語で簡潔にまとめます。

**カバーするトピック：**
- 🇮🇷 イラン・イスラエル情勢
- 🇺🇸 米国経済（株価、FRB、トランプ）
- 🇯🇵 日本経済（日経平均、市場動向）
- 🌤️ 天気（東京 + ニューヨーク）

---

## 📅 配信スケジュール

| 時間 | コンテンツ |
|------|-----------|
| **8:00 AM** | 朝のブリーフィング（戦争、経済、天気） |
| **12:00 PM** | 昼の更新（市場、戦争展開） |
| **4:00 PM** | 午後更新（市場途中、戦争） |
| **8:00 PM** | 夜まとめ（市場終値、1 日の総括） |

---

## 🚀 インストール

```bash
clawhub install japanese-news-briefing
```

または手動インストール：

```bash
mkdir -p ~/.openclaw/skills/japanese-news-briefing
cd ~/.openclaw/skills/japanese-news-briefing
# SKILL.md と clawhub.json を配置
```

---

## 📖 使い方

### 自動実行（推奨）

HEARTBEAT.md に設定を追加するだけで自動実行されます。

### 手動実行

```
/briefing morning    # 朝のニュース
/briefing noon       # 昼のニュース
/briefing afternoon  # 午後のニュース
/briefing evening    # 夜のニュース
```

---

## 📋 出力例

```
おはよう！朝のニュース 🖤

## 🇮🇷 イラン・イスラエル情勢
- 停戦交渉継続中、45 日間停戦を推進
- イラン「繰り返しパターン拒否」と表明

## 🇺🇸 米国経済
- ダウ平均 小幅安 (-0.1%)
- ナスダック +1.2%（週間で 4.3% 高）

## 🇯🇵 日本経済
- 日経平均 289 円高の 54,107 円 (+0.54%)
- 外国人売り増加、円安で圧力

## 🌤️ 天気
**東京** ☁️ 最高 22°C / 最低 12°C
**ニューヨーク** ☁️ 最高 12°C / 最低 2°C

---
**全体として:** 停戦交渉は継続中も、イランは慎重姿勢
```

---

## ⚙️ 設定

### カスタマイズ

HEARTBEAT.md を編集：

```markdown
## Notes
- Language: Japanese for all 4 briefings
- Run 4 times daily: 8am, 12pm, 4pm, 8pm
- Weather: Tokyo + New York City only
- Skip if checked <30 min ago
```

### 天気都市の変更

SKILL.md の天気セクションを編集：

```markdown
**東京** [天気]
**ニューヨーク** [天気]
**大阪** [天気]  # 追加
```

---

## 💰 価格

**無料** 🎉

- ✅ 無制限の自動実行
- ✅ 無料アップデート
- ✅ 日本語サポート

**Harinezumi の他のスキルもチェック！**

---

## ⚠️ 制限事項

- 深刻な天気警報はカバーしない
- 歴史データは取得不可
- 速報は 30 分以内のチェックをスキップ
- 中国語対応は別スキル

---

## 🆘 サポート

問題があれば：
- GitHub Issues: https://github.com/aoikawa/openclaw-skills/issues
- Discord: @aoikawa

---

## 📝 バージョン履歴

### v1.0.0 (2026-04-06)
- 初回リリース
- 1 日 4 回ブリーフィング
- 日本語対応
- 天気予報統合

---

## 👨‍💻 作者

**Harinezumi** - OpenClaw ユーザー、AMD GPU エンスージアスト

他のスキル：
- gpu-cleanup-tool（AMD GPU 向け）
- openclaw-optimizer（設定最適化）

---

**Enjoy your daily news! 🦞**
