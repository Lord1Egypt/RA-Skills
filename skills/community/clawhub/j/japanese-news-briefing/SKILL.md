# Japanese News Briefing

## What This Skill Does
1 日 4 回（朝・昼・午後・夜）自動でニュースを収集し、日本語で簡潔にまとめて配信します。イラン・イスラエル情勢、米国経済、日本経済、天気をカバー。

## Prerequisites
- OpenClaw 2026.3+
- ollama_web_search プラグインが有効
- 天気情報：wttr.in または Open-Meteo API

## How to Use It
このスキルは自動実行されます。手動でもトリガー可能：

```
/briefing morning    # 朝のニュース
/briefing noon       # 昼のニュース
/briefing afternoon  # 午後のニュース
/briefing evening    # 夜のニュース
```

## Schedule
- **8:00 AM** - 朝のブリーフィング（戦争、経済、天気）
- **12:00 PM** - 昼の更新（市場、戦争展開）
- **4:00 PM** - 午後更新（市場途中、戦争）
- **8:00 PM** - 夜まとめ（市場終値、1 日の総括）

## Output Format
```
おはよう！朝のニュース 🖤

## 🇮🇷 イラン・イスラエル情勢
- [主要ニュース 1]
- [主要ニュース 2]

## 🇺🇸 米国経済
- [株価動向]
- [経済指標]

## 🇯🇵 日本経済
- [日経平均]
- [主要トピック]

## 🌤️ 天気
**東京** [天気] 最高 X°C / 最低 Y°C
**ニューヨーク** [天気] 最高 X°C / 最低 Y°C

---
**全体として:** [1 行まとめ]
```

## Configuration
HEARTBEAT.md で設定をカスタマイズ：

```markdown
## Notes
- Language: Japanese for all 4 briefings
- Run 4 times daily: 8am, 12pm, 4pm, 8pm
- Weather: Tokyo + New York City only
```

## Limitations
- 深刻な天気警報はカバーしない
- 歴史データは取得不可
- 速報は 30 分以内のチェックをスキップ

## Rules
- 日本語で回答（ユーザーが中国語を要求しない限り）
- 各セクション 3-5 項目に制限
- 全体で 500 字以内
- ソースを明示
- 重複ニュースはスキップ
