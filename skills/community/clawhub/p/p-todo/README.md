# P-Todo

![Platform](https://img.shields.io/badge/Platform-Windows-blue?logo=windows)
![Java](https://img.shields.io/badge/Java-25-orange?logo=openjdk)
![JavaFX](https://img.shields.io/badge/JavaFX-26-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Release](https://img.shields.io/badge/Release-v1.0.0-brightgreen)

> 📖 **简体中文请查看：[说明.md](说明.md)**（项目完整文档、架构设计、开发指南）

---

## English

A lightweight, high-performance desktop todo application for individuals and small teams, built with modern JavaFX. Features a unique **mini floating window**, **color-coded priority system**, **9-language i18n**, and a full **REST API** for AI agent integration.

**Platform:** Windows | **Tech Stack:** Java 25 + JavaFX 26 + SQLite | **License:** MIT

### 🤖 AI Agent Integration

P-Todo provides a complete **REST API** (18 endpoints on port 9527) that allows AI agents to fully control the application — create, read, update, delete tasks, manage users, search, export data, and more.

**Quick example — AI creates a task:**
```bash
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Review PR #42","priority":"HIGH","assignee_id":"user-001"}'
```

For complete API documentation, see **[SKILL.md](SKILL.md)** — a ready-to-use skill file designed for AI agents (OpenClaw, Claude, GPT, etc.).

**What AI agents can do:**
- 📋 Create, edit, complete, delete tasks
- 🔍 Search tasks by keyword
- 👥 Manage team members
- 📊 Get statistics and analytics
- 📤 Export data as JSON or CSV
- 🌐 Switch the UI language in real-time
- 🔔 Get notifications for due/overdue tasks

### ✨ Features

- **Task Management** — Create, edit, complete, delete tasks with priorities, due dates, assignees, and tags
- **Color Priority System** — 4-tier auto-assigned colors: Gray (None) → Green (Low) → Yellow (Medium) → Red (High/Urgent)
- **Mini Window** — Always-on-top compact floating widget, no taskbar icon, drag-to-move, resizable
- **Multi-View Dashboard** — List, Kanban Board, Calendar (with Lunar Calendar), Statistics, Workbench
- **9-Language i18n** — 中文, 繁體中文, English, 日本語, 조선어, Français, Deutsch, Español, Português
- **REST API** — 18 endpoints for full CRUD, search, statistics, export, settings
- **Notification Sound** — Sound alerts for due and overdue tasks, customizable audio files
- **System Tray** — Minimize to tray, quick access via tray menu
- **Keyboard Shortcuts** — Ctrl+N (new), Ctrl+K (search), Ctrl+M (mini window), Enter (toggle complete)

### 📥 Download

Go to **[Releases](https://github.com/Pondsi/P-Todo/releases/tag/v1.0.0)** to download:

| File | Size | Description |
|------|------|-------------|
| `P-Todo.exe` | 24 MB | Standalone executable, no Java installation required |
| `P-Todo-1.0.0-all-in-one.jar | 24.6 MB | All-in-one JAR, includes Java 25+ runtime, no installation needed |
| `P-Todo-1.0.0-source-only.jar` | 0.3 MB | Source-only JAR, requires Java 25+ and JavaFX 26 |

### 🚀 Quick Start

**Requirements:** Java 25+ (JDK), Maven 3.9+

```bash
# Clone the repository
git clone https://github.com/Pondsi/P-Todo.git
cd P-Todo

# Build
mvn compile
mvn package -DskipTests

# Run
java -jar target/P-Todo-1.0.0.jar
```

Or use the included scripts: `compile.bat` / `compile.ps1` (compile), `run_app.bat` (run), `run_debug.bat` (debug).

### 🔑 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New task |
| Ctrl+K | Global search |
| Ctrl+M | Toggle mini window / main window |
| Enter | Toggle task completion |
| Delete | Delete selected task |
| ↑ / ↓ | Navigate tasks |
| Esc | Close dialog |

### 📁 Project Structure

```
P-Todo/
├── src/main/java/com/teamtodo/
│   ├── App.java                    # Entry point
│   ├── api/ApiServer.java          # REST API (port 9527)
│   ├── controller/                 # JavaFX controllers (11 files)
│   ├── dao/                        # SQLite data access (5 files)
│   ├── model/                      # Data models + enums
│   ├── service/                    # Business logic (6 files)
│   └── util/                       # Utilities (i18n, calendar, export, etc.)
├── src/main/resources/
│   ├── css/style.css               # UI theme
│   ├── fxml/                       # 5 FXML layouts
│   ├── i18n/                       # 9 language files (344 keys)
│   └── icon.png                    # App icon
├── tools/                          # i18n helper scripts
├── pom.xml                         # Maven config
├── SKILL.md                        # REST API skill (for AI agents)
├── README.md                       # This file
├── LICENSE                         # MIT License
└── 说明.md                          # Full documentation (Chinese)
```

### ⚙️ Database

- **Engine:** SQLite with HikariCP connection pool
- **Location:** `~/P-Todo/data/P-Todo.db`
- **Tables:** todos, users, comments, reminders, activity_log (reserved)

### 📚 Documentation

- [说明.md](说明.md) — Complete documentation (architecture, i18n guide, extension guide)
- [SKILL.md](SKILL.md) — REST API skill for AI agents

### ⚠️ Known Issues

- IME candidate window does not follow cursor position (JavaFX 26 known issue)
- High-DPI display may have drag offset on mini window

### 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📄 License

[MIT](LICENSE) — Copyright (c) 2026 **Pondsi**

💖 [Sponsors](SPONSORS.md)

---

## 繁體中文

輕量、高效能的桌面待辦事項管理應用程式，專為個人和小型團隊設計，採用現代 JavaFX 構建。具獨特的**迷你浮動視窗**、**顏色優先順序系統**、**9 語言國際化**及完整的 **REST API** 供 AI 智能體整合使用。

**平台：** Windows | **技術棧：** Java 25 + JavaFX 26 + SQLite | **授權條款：** MIT

### 🤖 AI 智能體整合

P-Todo 提供完整的 **REST API**（連接埠 9527，18 個端點），讓 AI 智能體能完全控制應用程式——建立、讀取、更新、刪除任務，管理使用者，搜尋、匯出資料等。

**快速範例——AI 建立任務：**
```bash
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"審查 PR #42","priority":"HIGH","assignee_id":"user-001"}'
```

完整 API 文件請參閱 **[SKILL.md](SKILL.md)**——專為 AI 智能體（OpenClaw、Claude、GPT 等）設計的技能文件。

**AI 智能體可以做的事：**
- 📋 建立、編輯、完成、刪除任務
- 🔍 關鍵字搜尋任務
- 👥 管理團隊成員
- 📊 取得統計與分析
- 📤 匯出 JSON 或 CSV 資料
- 🌐 即時切換介面語言
- 🔔 取得到期/逾期任務通知

### ✨ 主要功能

- **待辦管理** — 建立、編輯、完成、刪除任務，支援優先順序、截止日期、負責人、標籤
- **顏色優先順序系統** — 四級自動分配色彩：灰色（無）→ 綠色（低）→ 黃色（中）→ 紅色（高/緊急）
- **迷你視窗** — 永遠置頂的緊湊浮動小工具，不在工作列顯示，可拖曳、調整大小
- **多視圖儀表板** — 清單、看板、日曆（含農曆）、統計、工作台
- **9 語言國際化** — 中文、繁體中文、English、日本語、조선어、Français、Deutsch、Español、Português
- **REST API** — 18 個端點，完整 CRUD、搜尋、統計、匯出、設定
- **通知音效** — 逾期和到期任務的聲音提醒，可自訂音訊檔案
- **系統托盤** — 最小化到托盤，透過托盤選單快速存取
- **快捷鍵** — Ctrl+N（新建）、Ctrl+K（搜尋）、Ctrl+M（迷你視窗）、Enter（切換完成）

### 📥 下載

前往 **[Releases](https://github.com/Pondsi/P-Todo/releases/tag/v1.0.0)** 下載：

| 檔案 | 大小 | 說明 |
|------|------|------|
| `P-Todo.exe` | 24 MB | 獨立可執行檔，無需安裝 Java |
| `P-Todo-1.0.0-all-in-one.jar | 24.6 MB | 整合版 JAR，已包含 Java 25+ 執行環境，無需安裝 |
| `P-Todo-1.0.0-source-only.jar` | 0.3 MB | 僅原始碼 JAR，需要 Java 25+ 及 JavaFX 26 |

### 🚀 快速開始

**系統需求：** Java 25+（JDK）、Maven 3.9+

```bash
git clone https://github.com/Pondsi/P-Todo.git
cd P-Todo
mvn compile
mvn package -DskipTests
java -jar target/P-Todo-1.0.0.jar
```

或使用內建腳本：`compile.bat` / `compile.ps1`（編譯）、`run_app.bat`（執行）、`run_debug.bat`（偵錯）。

### 🔑 快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| Ctrl+N | 新建待辦 |
| Ctrl+K | 全局搜尋 |
| Ctrl+M | 切換迷你視窗/主視窗 |
| Enter | 切換完成狀態 |
| Delete | 刪除選取待辦 |
| ↑ / ↓ | 上下選擇待辦 |
| Esc | 關閉彈窗 |

### 📁 專案結構

```
P-Todo/
├── src/main/java/com/teamtodo/
│   ├── App.java                    # 入口點
│   ├── api/ApiServer.java          # REST API（連接埠 9527）
│   ├── controller/                 # JavaFX 控制器（11 個檔案）
│   ├── dao/                        # SQLite 資料存取（5 個檔案）
│   ├── model/                      # 資料模型 + 列舉
│   ├── service/                    # 業務邏輯（6 個檔案）
│   └── util/                       # 工具類（國際化、日曆、匯出等）
├── src/main/resources/
│   ├── css/style.css               # UI 主題
│   ├── fxml/                       # 5 個 FXML 佈局
│   ├── i18n/                       # 9 種語言檔案（344 個 key）
│   └── icon.png                    # 應用圖示
├── tools/                          # 國際化輔助腳本
├── pom.xml                         # Maven 設定
├── SKILL.md                        # REST API 技能（供 AI 智能體使用）
├── README.md                       # 本檔案
├── LICENSE                         # MIT 授權條款
└── 说明.md                          # 完整中文文件
```

### 📚 文件

- [说明.md](说明.md) — 完整文件（架構、國際化指南、擴充指南）
- [SKILL.md](SKILL.md) — REST API 技能（供 AI 智能體使用）

### ⚠️ 已知問題

- IME 候選視窗不跟隨游標位置（JavaFX 26 已知問題）
- 高 DPI 顯示器上迷你視窗拖曳可能有偏移

### 🤝 貢獻

1. Fork 儲存庫
2. 建立功能分支（`git checkout -b feature/amazing-feature`）
3. 提交變更（`git commit -m '新增某項功能'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 開啟 Pull Request

### 📄 授權條款

[MIT](LICENSE) — Copyright (c) 2026 **Pondsi**

💖 [贊助者](SPONSORS.md)

---

## 日本語

軽量・高性能なデスクトップ用タスク管理アプリケーション。個人〜小規模チーム向けにモダンな JavaFX で構築。ユニークな**ミニフローティングウィンドウ**、**カラーリング優先度システム**、**9言語国際化**、AIエージェント向けの完全な**REST API**を備えています。

**プラットフォーム：** Windows | **技術スタック：** Java 25 + JavaFX 26 + SQLite | **ライセンス：** MIT

### 🤖 AIエージェント統合

P-Todoは、AIエージェントがアプリケーションを完全に制御できる**REST API**（ポート9527、18エンドポイント）を提供します。タスクの作成、読み取り、更新、削除、ユーザー管理、検索、データエクスポートが可能です。

**クイック例——AIがタスクを作成：**
```bash
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"PR #42をレビュー","priority":"HIGH","assignee_id":"user-001"}'
```

完全なAPIドキュメントは **[SKILL.md](SKILL.md)** を参照——AIエージェント（OpenClaw、Claude、GPT等）向けに設計されたスキルファイルです。

**AIエージェントができること：**
- 📋 タスクの作成、編集、完了、削除
- 🔍 キーワードでタスク検索
- 👥 チームメンバーの管理
- 📊 統計と分析の取得
- 📤 JSON/CSV形式でデータエクスポート
- 🌐 UI言語をリアルタイムで切り替え
- 🔔 期限到達・超過タスクの通知受信

### ✨ 主な機能

- **タスク管理** — 優先度、期限、担当者、タグ付きタスクの作成、編集、完了、削除
- **カラーリング優先度システム** — 4段階自動割り当て：グレー（なし）→ 緑（低）→ 黄（中）→ 赤（高/緊急）
- **ミニウィンドウ** — 常に最前面のコンパクトフローティングウィジェット、タスクバー非表示、ドラッグ移動、リサイズ可能
- **マルチビューダッシュボード** — リスト、カンバン、カレンダー（旧暦対応）、統計、ワークベンチ
- **9言語国際化** — 中文、繁體中文、English、日本語、조선어、Français、Deutsch、Español、Português
- **REST API** — 18エンドポイント、完全なCRUD、検索、統計、エクスポート、設定
- **通知音** — 期限到達・超過タスクのサウンドアラート、カスタマイズ可能
- **システムトレイ** — トレイに最小化、トレイメニューから素早くアクセス
- **キーボードショートカット** — Ctrl+N（新規）、Ctrl+K（検索）、Ctrl+M（ミニウィンドウ）、Enter（完了切替）

### 📥 ダウンロード

**[Releases](https://github.com/Pondsi/P-Todo/releases/tag/v1.0.0)** からダウンロード：

| ファイル | サイズ | 説明 |
|---------|--------|------|
| `P-Todo.exe` | 24 MB | スタンドアロン実行ファイル、Java不要 |
| `P-Todo-1.0.0-all-in-one.jar | 24.6 MB | オールインワンJAR、Java 25+ を含む、インストール不要 |
| `P-Todo-1.0.0-source-only.jar` | 0.3 MB | ソースのみJAR、Java 25+ と JavaFX 26 必須 |

### 🚀 クイックスタート

**前提条件：** Java 25+（JDK）、Maven 3.9+

```bash
git clone https://github.com/Pondsi/P-Todo.git
cd P-Todo
mvn compile
mvn package -DskipTests
java -jar target/P-Todo-1.0.0.jar
```

または内蔵スクリプトを使用：`compile.bat` / `compile.ps1`（コンパイル）、`run_app.bat`（実行）、`run_debug.bat`（デバッグ）。

### 🔑 キーボードショートカット

| ショートカット | アクション |
|---------------|-----------|
| Ctrl+N | 新規タスク |
| Ctrl+K | グローバル検索 |
| Ctrl+M | ミニウィンドウ/メインウィンドウ切替 |
| Enter | 完了状態切替 |
| Delete | 選択タスク削除 |
| ↑ / ↓ | タスクを上下選択 |
| Esc | ダイアログを閉じる |

### 📁 プロジェクト構造

```
P-Todo/
├── src/main/java/com/teamtodo/
│   ├── App.java                    # エントリポイント
│   ├── api/ApiServer.java          # REST API（ポート9527）
│   ├── controller/                 # JavaFXコントローラー（11ファイル）
│   ├── dao/                        # SQLiteデータアクセス（5ファイル）
│   ├── model/                      # データモデル + 列挙型
│   ├── service/                    # ビジネスロジック（6ファイル）
│   └── util/                       # ユーティリティ（i18n、カレンダー、エクスポート等）
├── src/main/resources/
│   ├── css/style.css               # UIテーマ
│   ├── fxml/                       # FXMLレイアウト（5ファイル）
│   ├── i18n/                       # 9言語ファイル（344キー）
│   └── icon.png                    # アプリアイコン
├── tools/                          # i18nヘルパースクリプト
├── pom.xml                         # Maven設定
├── SKILL.md                        # REST APIスキル（AIエージェント向け）
├── README.md                       # 本ファイル
├── LICENSE                         # MITライセンス
└── 说明.md                          # 完全な説明書（中文）
```

### 📚 ドキュメント

- [说明.md](说明.md) — 完全なドキュメント（アーキテクチャ、i18nガイド、拡張ガイド）
- [SKILL.md](SKILL.md) — REST APIスキル（AIエージェント向け）

### ⚠️ 既知の問題

- IME候補ウィンドウがカーソルに追従しない（JavaFX 26の既知バグ）
- 高DPI表示でミニウィンドウのドラッグにオフセットが発生

### 📄 ライセンス

[MIT](LICENSE) — Copyright (c) 2026 **Pondsi**

💖 [スポンサー](SPONSORS.md)

---

## 조선어

경량·고성능 데스크톱 할일 관리 앱. 개인 및 소규모 팀을 위해 모던 JavaFX로 구축. 고유의 **미니 플로팅 윈도우**, **색상 우선순위 시스템**, **9개 언어 국제화**, AI 에이전트 통합을 위한 완전한 **REST API**를 제공합니다.

**플랫폼:** Windows | **기술 스택:** Java 25 + JavaFX 26 + SQLite | **라이선스:** MIT

### 🤖 AI 에이전트 통합

P-Todo는 AI 에이전트가 애플리케이션을 완전히 제어할 수 있는 **REST API** (포트 9527, 18개 엔드포인트)를 제공합니다. 작업 생성, 읽기, 업데이트, 삭제, 사용자 관리, 검색, 데이터 내보내기가 가능합니다.

**빠른 예시 — AI가 작업 생성:**
```bash
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"PR #42 검토","priority":"HIGH","assignee_id":"user-001"}'
```

완전한 API 문서는 **[SKILL.md](SKILL.md)**를 참조하세요 — AI 에이전트(OpenClaw, Claude, GPT 등)를 위해 설계된 스킬 파일입니다.

**AI 에이전트가 할 수 있는 것:**
- 📋 작업 생성, 편집, 완료, 삭제
- 🔍 키워드로 작업 검색
- 👥 팀 구성원 관리
- 📊 통계 및 분석 조회
- 📤 JSON 또는 CSV로 데이터 내보내기
- 🌐 UI 언어 실시간 전환
- 🔔 마감 및 기한 초과 작업 알림 수신

### ✨ 주요 기능

- **할일 관리** — 우선순위, 마감일, 담당자, 태그가 포함된 작업 생성, 편집, 완료, 삭제
- **색상 우선순위 시스템** — 4단계 자동 색상: 회색(없음) → 녹색(낮음) → 노란색(보통) → 빨간색(높음/긴급)
- **미니 창** — 항상 최상위의 컴팩트한 플로팅 위젯, 작업 표시줄 아이콘 없음, 드래그 이동, 크기 조절 가능
- **다중 뷰 대시보드** — 목록, 칸반 보드, 달력(음력 포함), 통계, 워크벤치
- **9개 언어 국제화** — 中文, 繁體中文, English, 日本語, 조선어, Français, Deutsch, Español, Português
- **REST API** — 18개 엔드포인트, 완전한 CRUD, 검색, 통계, 내보내기, 설정
- **알림 소리** — 마감 및 기한 초과 작업에 대한 사운드 알림, 사용자 지정 가능
- **시스템 트레이** — 트레이로 최소화, 트레이 메뉴로 빠른 접근
- **키보드 단축키** — Ctrl+N(새 작업), Ctrl+K(검색), Ctrl+M(미니 창), Enter(완료 전환)

### 📥 다운로드

**[Releases](https://github.com/Pondsi/P-Todo/releases/tag/v1.0.0)**에서 다운로드:

| 파일 | 크기 | 설명 |
|------|------|------|
| `P-Todo.exe` | 24 MB | 스탠드얼론 실행 파일, Java 불필요 |
| `P-Todo-1.0.0-all-in-one.jar | 24.6 MB | 올인원 JAR, Java 25+ 포함, 설치 불필요 필요 |
| `P-Todo-1.0.0-source-only.jar` | 0.3 MB | 소스만 JAR, Java 25+ 및 JavaFX 26 필요 |

### 🚀 빠른 시작

**필수 조건:** Java 25+ (JDK), Maven 3.9+

```bash
git clone https://github.com/Pondsi/P-Todo.git
cd P-Todo
mvn compile
mvn package -DskipTests
java -jar target/P-Todo-1.0.0.jar
```

또는 내장 스크립트 사용: `compile.bat` / `compile.ps1` (컴파일), `run_app.bat` (실행), `run_debug.bat` (디버그).

### 🔑 키보드 단축키

| 단축키 | 동작 |
|--------|------|
| Ctrl+N | 새 작업 |
| Ctrl+K | 글로벌 검색 |
| Ctrl+M | 미니 창/메인 창 전환 |
| Enter | 완료 상태 전환 |
| Delete | 선택 작업 삭제 |
| ↑ / ↓ | 작업 상하 이동 |
| Esc | 대화 상자 닫기 |

### 📁 프로젝트 구조

```
P-Todo/
├── src/main/java/com/teamtodo/
│   ├── App.java                    # 진입점
│   ├── api/ApiServer.java          # REST API (포트 9527)
│   ├── controller/                 # JavaFX 컨트롤러 (11개 파일)
│   ├── dao/                        # SQLite 데이터 액세스 (5개 파일)
│   ├── model/                      # 데이터 모델 + 열거형
│   ├── service/                    # 비즈니스 로직 (6개 파일)
│   └── util/                       # 유틸리티 (다국어, 달력, 내보내기 등)
├── src/main/resources/
│   ├── css/style.css               # UI 테마
│   ├── fxml/                       # FXML 레이아웃 (5개 파일)
│   ├── i18n/                       # 9개 언어 파일 (344 키)
│   └── icon.png                    # 앱 아이콘
├── tools/                          # 다국어 도움말 스크립트
├── pom.xml                         # Maven 설정
├── SKILL.md                        # REST API 스킬 (AI 에이전트용)
├── README.md                       # 이 파일
├── LICENSE                         # MIT 라이선스
└── 说明.md                          # 전체 문서 (중국어)
```

### 📚 문서

- [说明.md](说明.md) — 전체 문서 (아키텍처, 다국어 가이드, 확장 가이드)
- [SKILL.md](SKILL.md) — REST API 스킬 (AI 에이전트용)

### ⚠️ 알려진 문제

- IME 후보 창이 커서를 따라가지 않음 (JavaFX 26 알려진 버그)
- 고DPI 디스플레이에서 미니 창 드래그 오프셋 발생 가능

### 📄 라이선스

[MIT](LICENSE) — Copyright (c) 2026 **Pondsi**

💖 [후원자](SPONSORS.md)

---

## Français

Application légère et performante de gestion de tâches de bureau pour les particuliers et les petites équipes, construite avec JavaFX moderne. Dispose d'une **mini fenêtre flottante** unique, d'un **système de couleurs par priorité**, d'une **internationalisation en 9 langues** et d'une **REST API** complète pour l'intégration d'agents IA.

**Plateforme :** Windows | **Stack technique :** Java 25 + JavaFX 26 + SQLite | **Licence :** MIT

### 🤖 Intégration d'agents IA

P-Todo fournit une **REST API** complète (port 9527, 18 points de terminaison) permettant aux agents IA de contrôler entièrement l'application — créer, lire, modifier, supprimer des tâches, gérer les utilisateurs, rechercher, exporter des données, etc.

**Exemple rapide — L'IA crée une tâche :**
```bash
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Revoir la PR #42","priority":"HIGH","assignee_id":"user-001"}'
```

Pour la documentation complète de l'API, consultez **[SKILL.md](SKILL.md)** — un fichier de compétence conçu pour les agents IA (OpenClaw, Claude, GPT, etc.).

**Ce que les agents IA peuvent faire :**
- 📋 Créer, modifier, compléter, supprimer des tâches
- 🔍 Rechercher des tâches par mot-clé
- 👥 Gérer les membres de l'équipe
- 📊 Obtenir des statistiques et analyses
- 📤 Exporter les données en JSON ou CSV
- 🌐 Changer la langue de l'interface en temps réel
- 🔔 Recevoir des notifications pour les tâches dues et en retard

### ✨ Fonctionnalités

- **Gestion des tâches** — Créer, modifier, compléter, supprimer avec priorités, dates limites, assignataires et tags
- **Système de couleurs** — Codage à 4 niveaux : Gris (Aucun) → Vert (Faible) → Jaune (Moyen) → Rouge (Élevé/Urgent)
- **Mini fenêtre** — Widget flottant compact toujours au premier plan, pas d'icône dans la barre des tâches
- **Tableau de bord multi-vues** — Liste, Kanban, Calendrier (avec calendrier lunaire), Statistiques, Table de travail
- **Internationalisation 9 langues** — 中文, 繁體中文, English, 日本語, 조선어, Français, Deutsch, Español, Português
- **REST API** — 18 points de terminaison, CRUD complet, recherche, statistiques, exportation, paramètres
- **Son de notification** — Alertes sonores pour les tâches à échéance et en retard
- **Systray** — Réduction dans la zone de notification, accès rapide via le menu
- **Raccourcis clavier** — Ctrl+N (nouveau), Ctrl+K (recherche), Ctrl+M (mini fenêtre), Enter (basculer)

### 📥 Téléchargement

Rendez-vous sur **[Releases](https://github.com/Pondsi/P-Todo/releases/tag/v1.0.0)** pour télécharger :

| Fichier | Taille | Description |
|---------|--------|-------------|
| `P-Todo.exe` | 24 Mo | Exécutable autonome, pas besoin de Java |
| `P-Todo-1.0.0-all-in-one.jar | 24.6 Mo | JAR tout-en-un, inclut Java 25+, aucune installation requise |
| `P-Todo-1.0.0-source-only.jar` | 0.3 Mo | JAR source uniquement, nécessite Java 25+ et JavaFX 26 |

### 🚀 Démarrage rapide

**Prérequis :** Java 25+ (JDK), Maven 3.9+

```bash
git clone https://github.com/Pondsi/P-Todo.git
cd P-Todo
mvn compile
mvn package -DskipTests
java -jar target/P-Todo-1.0.0.jar
```

Ou utilisez les scripts inclus : `compile.bat` / `compile.ps1` (compiler), `run_app.bat` (exécuter), `run_debug.bat` (déboguer).

### 🔑 Raccourcis clavier

| Raccourci | Action |
|-----------|--------|
| Ctrl+N | Nouvelle tâche |
| Ctrl+K | Recherche globale |
| Ctrl+M | Basculer mini fenêtre / fenêtre principale |
| Enter | Basculer l'achèvement |
| Delete | Supprimer la tâche sélectionnée |
| ↑ / ↓ | Naviguer entre les tâches |
| Esc | Fermer la boîte de dialogue |

### 📄 Licence

[MIT](LICENSE) — Copyright (c) 2026 **Pondsi**

💖 [Sponsors](SPONSORS.md)

---

## Deutsch

Leichtgewichtige, leistungsstarke Desktop-ToDo-Anwendung für Einzelpersonen und kleine Teams, gebaut mit modernem JavaFX. Mit einzigartigem **Mini-Schwebefenster**, **Farbprioritätssystem**, **9-Sprachen-i18n** und vollständiger **REST API** für die KI-Agenten-Integration.

**Plattform:** Windows | **Tech-Stack:** Java 25 + JavaFX 26 + SQLite | **Lizenz:** MIT

### 🤖 KI-Agenten-Integration

P-Todo bietet eine vollständige **REST API** (Port 9527, 18 Endpunkte), mit der KI-Agenten die Anwendung vollständig steuern können — Aufgaben erstellen, lesen, aktualisieren, löschen, Benutzer verwalten, suchen, Daten exportieren und mehr.

**Schnelles Beispiel — KI erstellt eine Aufgabe:**
```bash
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"PR #42 überprüfen","priority":"HIGH","assignee_id":"user-001"}'
```

Vollständige API-Dokumentation siehe **[SKILL.md](SKILL.md)** — eine einsatzbereite Skill-Datei für KI-Agenten (OpenClaw, Claude, GPT etc.).

**Was KI-Agenten können:**
- 📋 Aufgaben erstellen, bearbeiten, abschließen, löschen
- 🔍 Aufgaben nach Stichwort suchen
- 👥 Teammitglieder verwalten
- 📊 Statistiken und Analysen abrufen
- 📤 Daten als JSON oder CSV exportieren
- 🌐 UI-Sprache in Echtzeit wechseln
- 🔔 Benachrichtigungen für fällige und überfällige Aufgaben erhalten

### ✨ Funktionen

- **Aufgabenverwaltung** — Erstellen, Bearbeiten, Abschließen, Löschen mit Prioritäten, Fälligkeiten, Zuständigen und Tags
- **Farbprioritätssystem** — 4-Stufen-Farbcodierung: Grau (Keine) → Grün (Niedrig) → Gelb (Mittel) → Rot (Hoch/Dringend)
- **Mini-Fenster** — Kompaktes, immer im Vordergrund schwebendes Widget, kein Taskleistensymbol
- **Mehransichten-Dashboard** — Liste, Kanban-Board, Kalender (mit Mondkalender), Statistiken, Arbeitsbereich
- **9-Sprachen-i18n** — 中文, 繁體中文, English, 日本語, 조선어, Français, Deutsch, Español, Português
- **REST API** — 18 Endpunkte, vollständiges CRUD, Suche, Statistiken, Export, Einstellungen
- **Benachrichtigungston** — Soundalarme für fällige und überfällige Aufgaben
- **Systemtray** — Minimierung in den Infobereich, schneller Zugriff über Tray-Menü
- **Tastenkürzel** — Ctrl+N (neu), Ctrl+K (suchen), Ctrl+M (Mini-Fenster), Enter (Abschluss umschalten)

### 📥 Download

Besuchen Sie **[Releases](https://github.com/Pondsi/P-Todo/releases/tag/v1.0.0)** zum Herunterladen:

| Datei | Größe | Beschreibung |
|-------|-------|-------------|
| `P-Todo.exe` | 24 MB | Eigenständige ausführbare Datei, kein Java nötig |
| `P-Todo-1.0.0-all-in-one.jar | 24.6 MB | All-in-One JAR, enthält Java 25+, keine Installation nötig |
| `P-Todo-1.0.0-source-only.jar` | 0.3 MB | Nur-Quellcode JAR, erfordert Java 25+ und JavaFX 26 |

### 🚀 Schnellstart

**Voraussetzungen:** Java 25+ (JDK), Maven 3.9+

```bash
git clone https://github.com/Pondsi/P-Todo.git
cd P-Todo
mvn compile
mvn package -DskipTests
java -jar target/P-Todo-1.0.0.jar
```

Oder verwenden Sie die mitgelieferten Skripte: `compile.bat` / `compile.ps1` (kompilieren), `run_app.bat` (ausführen), `run_debug.bat` (debuggen).

### 🔑 Tastenkürzel

| Kürzel | Aktion |
|--------|--------|
| Ctrl+N | Neue Aufgabe |
| Ctrl+K | Globale Suche |
| Ctrl+M | Mini-Fenster / Hauptfenster umschalten |
| Enter | Abschluss umschalten |
| Delete | Ausgewählte Aufgabe löschen |
| ↑ / ↓ | Aufgaben navigieren |
| Esc | Dialog schließen |

### 📄 Lizenz

[MIT](LICENSE) — Copyright (c) 2026 **Pondsi**

💖 [Sponsoren](SPONSORS.md)

---

## Español

Herramienta de gestión de tareas de escritorio ligera y de alto rendimiento para individuos y pequeños equipos, construida con JavaFX moderno. Cuenta con una **mini ventana flotante** única, **sistema de colores por prioridad**, **i18n en 9 idiomas** y una **REST API** completa para la integración de agentes de IA.

**Plataforma:** Windows | **Stack tecnológico:** Java 25 + JavaFX 26 + SQLite | **Licencia:** MIT

### 🤖 Integración de agentes de IA

P-Todo proporciona una **REST API** completa (puerto 9527, 18 endpoints) que permite a los agentes de IA controlar completamente la aplicación — crear, leer, actualizar, eliminar tareas, gestionar usuarios, buscar, exportar datos y más.

**Ejemplo rápido — La IA crea una tarea:**
```bash
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Revisar PR #42","priority":"HIGH","assignee_id":"user-001"}'
```

Para la documentación completa de la API, consulte **[SKILL.md](SKILL.md)** — un archivo de habilidad diseñado para agentes de IA (OpenClaw, Claude, GPT, etc.).

**Lo que los agentes de IA pueden hacer:**
- 📋 Crear, editar, completar, eliminar tareas
- 🔍 Buscar tareas por palabra clave
- 👥 Gestionar miembros del equipo
- 📊 Obtener estadísticas y análisis
- 📤 Exportar datos como JSON o CSV
- 🌐 Cambiar el idioma de la interfaz en tiempo real
- 🔔 Recibir notificaciones de tareas vencidas y atrasadas

### ✨ Características

- **Gestión de tareas** — Crear, editar, completar, eliminar con prioridades, fechas límite, responsables y etiquetas
- **Sistema de colores** — Codificación de 4 niveles: Gris (Ninguno) → Verde (Bajo) → Amarillo (Medio) → Rojo (Alto/Urgente)
- **Mini ventana** — Widget flotante compacto siempre visible, sin icono en la barra de tareas
- **Panel multi-vista** — Lista, tablero Kanban, calendario (con calendario lunar), estadísticas, panel de trabajo
- **i18n de 9 idiomas** — 中文, 繁體中文, English, 日本語, 조선어, Français, Deutsch, Español, Português
- **REST API** — 18 endpoints, CRUD completo, búsqueda, estadísticas, exportación, configuración
- **Sonido de notificación** — Alertas sonoras para tareas vencidas y atrasadas
- **Bandeja del sistema** — Minimizar a la bandeja, acceso rápido mediante menú
- **Atajos de teclado** — Ctrl+N (nuevo), Ctrl+K (buscar), Ctrl+M (mini ventana), Enter (alternar)

### 📥 Descarga

Visite **[Releases](https://github.com/Pondsi/P-Todo/releases/tag/v1.0.0)** para descargar:

| Archivo | Tamaño | Descripción |
|---------|--------|-------------|
| `P-Todo.exe` | 24 MB | Ejecutable independiente, sin necesidad de Java |
| `P-Todo-1.0.0-all-in-one.jar | 24.6 MB | JAR todo-en-uno, incluye Java 25+, sin instalación |
| `P-Todo-1.0.0-source-only.jar` | 0.3 MB | JAR solo fuente, requiere Java 25+ y JavaFX 26 |

### 🚀 Inicio rápido

**Requisitos:** Java 25+ (JDK), Maven 3.9+

```bash
git clone https://github.com/Pondsi/P-Todo.git
cd P-Todo
mvn compile
mvn package -DskipTests
java -jar target/P-Todo-1.0.0.jar
```

O use los scripts incluidos: `compile.bat` / `compile.ps1` (compilar), `run_app.bat` (ejecutar), `run_debug.bat` (depurar).

### 🔑 Atajos de teclado

| Atajo | Acción |
|-------|--------|
| Ctrl+N | Nueva tarea |
| Ctrl+K | Búsqueda global |
| Ctrl+M | Alternar mini ventana / ventana principal |
| Enter | Alternar finalización |
| Delete | Eliminar tarea seleccionada |
| ↑ / ↓ | Navegar entre tareas |
| Esc | Cerrar diálogo |

### 📄 Licencia

[MIT](LICENSE) — Copyright (c) 2026 **Pondsi**

💖 [Patrocinadores](SPONSORS.md)

---

## Português

Ferramenta de gerenciamento de tarefas de desktop leve e de alto desempenho para indivíduos e pequenas equipes, construída com JavaFX moderno. Possui **mini janela flutuante** exclusiva, **sistema de cores por prioridade**, **i18n em 9 idiomas** e uma **REST API** completa para integração com agentes de IA.

**Plataforma:** Windows | **Stack:** Java 25 + JavaFX 26 + SQLite | **Licença:** MIT

### 🤖 Integração com agentes de IA

O P-Todo fornece uma **REST API** completa (porta 9527, 18 endpoints) que permite aos agentes de IA controlar completamente o aplicativo — criar, ler, atualizar, excluir tarefas, gerenciar usuários, pesquisar, exportar dados e muito mais.

**Exemplo rápido — A IA cria uma tarefa:**
```bash
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Revisar PR #42","priority":"HIGH","assignee_id":"user-001"}'
```

Para documentação completa da API, consulte **[SKILL.md](SKILL.md)** — um arquivo de habilidade projetado para agentes de IA (OpenClaw, Claude, GPT, etc.).

**O que os agentes de IA podem fazer:**
- 📋 Criar, editar, concluir, excluir tarefas
- 🔍 Pesquisar tarefas por palavra-chave
- 👥 Gerenciar membros da equipe
- 📊 Obter estatísticas e análises
- 📤 Exportar dados como JSON ou CSV
- 🌐 Mudar o idioma da interface em tempo real
- 🔔 Receber notificações de tarefas vencidas e atrasadas

### ✨ Funcionalidades

- **Gerenciamento de tarefas** — Criar, editar, concluir, excluir com prioridades, datas limite, responsáveis e tags
- **Sistema de cores** — Codificação de 4 níveis: Cinza (Nenhum) → Verde (Baixo) → Amarelo (Médio) → Vermelho (Alto/Urgente)
- **Mini janela** — Widget flutuante compacto sempre no topo, sem ícone na barra de tarefas
- **Painel multi-visualização** — Lista, quadro Kanban, calendário (com calendário lunar), estatísticas, painel de trabalho
- **i18n de 9 idiomas** — 中文, 繁體中文, English, 日本語, 조선어, Français, Deutsch, Español, Português
- **REST API** — 18 endpoints, CRUD completo, pesquisa, estatísticas, exportação, configurações
- **Som de notificação** — Alertas sonoros para tarefas vencidas e atrasadas
- **Bandeja do sistema** — Minimizar para a bandeja, acesso rápido via menu
- **Atalhos de teclado** — Ctrl+N (novo), Ctrl+K (pesquisar), Ctrl+M (mini janela), Enter (alternar)

### 📥 Download

Acesse **[Releases](https://github.com/Pondsi/P-Todo/releases/tag/v1.0.0)** para baixar:

| Arquivo | Tamanho | Descrição |
|---------|---------|-----------|
| `P-Todo.exe` | 24 MB | Executável independente, sem necessidade de Java |
| `P-Todo-1.0.0-all-in-one.jar | 24.6 MB | JAR tudo-em-um, inclui Java 25+, sem necessidade de instalação |
| `P-Todo-1.0.0-source-only.jar` | 0.3 MB | JAR apenas código-fonte, requer Java 25+ e JavaFX 26 |

### 🚀 Início rápido

**Pré-requisitos:** Java 25+ (JDK), Maven 3.9+

```bash
git clone https://github.com/Pondsi/P-Todo.git
cd P-Todo
mvn compile
mvn package -DskipTests
java -jar target/P-Todo-1.0.0.jar
```

Ou use os scripts inclusos: `compile.bat` / `compile.ps1` (compilar), `run_app.bat` (executar), `run_debug.bat` (depurar).

### 🔑 Atalhos de teclado

| Atalho | Ação |
|--------|------|
| Ctrl+N | Nova tarefa |
| Ctrl+K | Pesquisa global |
| Ctrl+M | Alternar mini janela / janela principal |
| Enter | Alternar conclusão |
| Delete | Excluir tarefa selecionada |
| ↑ / ↓ | Navegar entre tarefas |
| Esc | Fechar diálogo |

### 📄 Licença

[MIT](LICENSE) — Copyright (c) 2026 **Pondsi**

💖 [Patrocinadores](SPONSORS.md)
