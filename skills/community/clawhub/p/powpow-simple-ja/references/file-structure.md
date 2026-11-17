# ファイル構成

> メンテナンス／トラブルシューティング専用。SKILL.md の実行時にこのファイルを読む必要はありません。

```
powpow-simple-ja/
├── SKILL.md                          # 本体（軽量に維持。詳細は references/）
├── config.json                       # platformUrl + ユーザー任意の Unsplash キー（機密情報なし。読み取り専用）
├── scripts/
│   ├── doctor.js                     # 初回実行セルフチェック（node/設定/ネットワーク/セッション）
│   ├── login.js                      # username/password → JWT（パスワードは保存しない、隠し入力）
│   ├── compose.js                    # 1コマンドで投稿HTMLを組み立てる（唯一の対応方法。完全にローカル）
│   ├── publish.js                    # ローカル画像のアップロード + ログインユーザーとして POST /api/posts
│   ├── verify.js                     # IDで投稿をプラットフォームAPI経由で検証
│   ├── delete-post.js                # 自身の投稿の削除（テスト後片付け）
│   ├── geocode.js                    # 地名 → WGS-84候補（ユーザーが選択）
│   ├── list-digital-humans.js        # ヘルスフィルター付き一覧／検索
│   ├── match-digital-human.js        # テーマ → 整列された健全な候補
│   ├── create-digital-human.js       # マップ用デジタルヒューマン作成（バッジ2個、30日失効。アバター: 生成/アップロード/URL）
│   ├── search-image.js               # Unsplash（ユーザー自身のキー、省略可。写真ページリンクの解決にも対応）
│   ├── upload-image.js               # ローカル画像 → プラットフォームストレージ → 公開URL（publish.js が使用）
│   └── lib/
│       ├── api-client.js             # プラットフォームAPIクライアント（JWT、ヘッダー固定）
│       ├── dh-match.js               # 共通のDHヘルスフィルター + テーマランキング（名前3倍、説明1倍、専門用語マスキング）
│       ├── coord-transform.js        # GCJ-02 ↔ WGS-84 変換（反復逆算）
│       └── html-formatter.js         # HTMLコンポーネント + CJK対応文字数カウント
└── references/
    ├── changelog.md                  # バージョン履歴（本パッケージ: 1.0.0。継承: 5.3 → 5.7.3）
    ├── security.md                   # セキュリティ設計 + プラットフォームAPI一覧
    ├── screenshots.md                # 製品スクリーンショット一覧 + 外部リンク
    └── file-structure.md             # このファイル
```

注: ログインセッション（`session.json`）は**スキルパッケージ内には決して書かれません**。
ユーザーのステートディレクトリ（`POWPOW_STATE_DIR`、デフォルト `~/.powpow/`）に保存され、
約7日で失効します（スキルは再ログインに6日間のマージンを確保しています）。

本パッケージのスクリプトは `powpow-simple` v5.7.3 とバイト単位で同一です —
異なるのはドキュメントとメタデータのみです。
