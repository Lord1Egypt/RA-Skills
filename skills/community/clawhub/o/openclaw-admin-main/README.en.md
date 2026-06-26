# OpenClaw Admin - AI Agent Management Platform

<p align="center">
  <strong>Modern AI Agent Gateway Management Console</strong>
</p>

<p align="center">
  <a href="https://github.com/itq5/OpenClaw-Admin">GitHub</a> •
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#project-structure">Project Structure</a> •
  <a href="#development-guide">Development Guide</a> •
  <a href="README.md">中文</a>
</p>

***

## Introduction

OpenClaw Admin is a modern AI agent management platform built with Vue 3, providing a complete web management interface for OpenClaw Gateway. Through intuitive visual operations, users can easily manage AI agents, sessions, models, channels, skills, and other core features.

### Version Compatibility

| OpenClaw Admin | OpenClaw Gateway | Status     |
| -------------- | ---------------- | ---------- |
| 0.2.6          | 2026.4.5         | ✅ Verified |

> 💡 **Tip**: It is recommended to use the latest version of OpenClaw Gateway for the best experience. If you encounter connection issues, please check if the Gateway version is compatible, or view the [OpenClaw Changelog](https://github.com/openclaw/openclaw/releases).

### Highlights

- 🎯 **All-in-One Management**: Integrated agent management, session monitoring, model configuration, channel management, and more
- 🌐 **Multi-Channel Support**: Supports QQ, Feishu, DingTalk, WeCom, and other message channels
- 🤖 **Multi-Agent Collaboration**: Create and manage multiple AI agents for complex task collaboration
- 📊 **Real-time Monitoring**: System resources, session status, token usage, and more
- 🌍 **Internationalization**: Built-in Chinese and English support, seamless switching
- 🎨 **Modern UI**: Responsive design based on Naive UI, supports light/dark themes

***

## Features

### Login

![Login](docs/images/登录.png)

- Username/password authentication
- Secure session management

### Dashboard

![Dashboard](docs/images/仪表盘.png)

- Runtime overview and key metrics
- Token usage trend charts
- Session activity statistics
- Real-time event stream monitoring
- Top models/channels/tools distribution

### Chat

![Chat](docs/images/在线对话.png)

- Real-time chat interface
- Support for slash commands (`/new`, `/skill`, `/model`, `/status`, `/subagents`)
- Message filtering and search
- Quick replies
- Real-time token usage statistics

### Sessions

![Sessions](docs/images/会话管理.png)

- Session list and details
- Create, reset, delete sessions
- Multi-dimensional filtering and sorting
- Message history export

### Memory

![Memory](docs/images/记忆管理.png)

- Agent document management
- Edit AGENTS, SOUL, IDENTITY, USER, and other core documents
- Markdown editor
- Quick template snippets

### Cron

![Cron](docs/images/计划任务.png)

- Scheduled task creation and management
- Support for Cron expressions, fixed intervals, specific times
- Task execution history
- Quick templates (morning report, health check, etc.)

### Models

![Models](docs/images/模型管理.png)

- Multi-model channel configuration
- API Key security management (masked display)
- Model probing
- Default model settings
- Coding package quick configuration

### Channels

![Channels](docs/images/频道管理.png)

- QQ, Feishu, DingTalk, WeCom channel configuration
- Channel status monitoring
- Credential security management
- One-click installation and configuration

### Skills

![Skills](docs/images/技能管理.png)

- Skill plugin list
- Built-in/user skill classification
- Skill installation and updates
- Chat visibility control

### Agents

![Agents](docs/images/多智能体.png)

- Agent creation and management
- Identity, model, tool permission configuration
- Session statistics and token usage
- Workspace file management

### Office

![Office-1](docs/images/智能体工坊-1.png)
![Office-2](docs/images/智能体工坊-2.png)

- Multi-agent collaboration space
- Scene creation wizard
- Task delegation and execution
- Inter-agent communication
- Team management

### MyWorld

![MyWorld](docs/images/虚拟公司.png)

- Visual office scenes
- Character movement and interaction
- Area interaction features
- Real-time communication

### Terminal

![Terminal](docs/images/远程终端.png)

- SSE protocol remote terminal
- Multi-node support
- Full-screen mode
- Custom shell and working directory

### Remote Desktop

![Remote Desktop](docs/images/远程桌面.png)

- Linux/Windows remote desktop
- Real-time screen transmission
- Mouse and keyboard operations
- Clipboard synchronization

### Files

![Files](docs/images/文件浏览器.png)

- Workspace file browsing
- File editing and preview
- File upload and download
- Directory management

### System

![System](docs/images/系统监视器.png)

- CPU, memory, disk usage
- Network connection status
- Instance online status
- Runtime statistics

### Settings

![Settings](docs/images/系统设置.png)

- Connection configuration management
- Appearance and theme settings
- Environment variable configuration

***

## Tech Stack

### Frontend Framework

| Technology | Version | Description                         |
| ---------- | ------- | ----------------------------------- |
| Vue        | 3.5.x   | Progressive JavaScript Framework    |
| Vue Router | 4.x     | Official Router                     |
| Pinia      | 3.x     | State Management                    |
| TypeScript | 5.x     | Type-safe JavaScript Superset       |
| Vite       | 7.x     | Next-generation Frontend Build Tool |

### UI Components

| Technology        | Version | Description             |
| ----------------- | ------- | ----------------------- |
| Naive UI          | 2.43.x  | Vue 3 Component Library |
| @vicons/ionicons5 | 0.13.x  | Icon Library            |
| @fortawesome      | 7.x     | Font Awesome Icons      |

### Communication & Data

| Technology  | Version | Description                           |
| ----------- | ------- | ------------------------------------- |
| WebSocket   | -       | Real-time Bidirectional Communication |
| SSE         | -       | Server-Sent Events                    |
| markdown-it | 14.x    | Markdown Parser                       |

### Backend Services

| Technology     | Version | Description              |
| -------------- | ------- | ------------------------ |
| Express        | 5.x     | Node.js Web Framework    |
| ws             | 8.x     | WebSocket Implementation |
| better-sqlite3 | 12.x    | SQLite Database          |
| node-pty       | 1.x     | Pseudo Terminal Support  |
| ssh2           | 1.x     | SSH Client               |

### Terminal

| Technology             | Version | Description       |
| ---------------------- | ------- | ----------------- |
| @xterm/xterm           | 6.x     | Terminal Emulator |
| @xterm/addon-fit       | 0.11.x  | Terminal Fit      |
| @xterm/addon-web-links | 0.12.x  | Link Support      |

***

## Quick Start

### Requirements

- Node.js >= 18.0.0
- npm >= 9.0.0

### Install Dependencies

```bash
npm install
```

### Initialize Environment Variables

```bash
cp .env.example .env
```

### Development Mode

Start frontend development server:

```bash
npm run dev
```

Start backend server:

```bash
npm run dev:server
```

Start both frontend and backend:

```bash
npm run dev:all
```

Visit `http://localhost:3000` to access the management interface.

### Production Build

```bash
npm run build
```

### Preview Build

```bash
npm run preview
```

***

## Project Structure

```
openclaw-admin/
├── src/
│   ├── api/                    # API Layer
│   │   ├── types/              # TypeScript Type Definitions
│   │   ├── connect.ts          # Connection Management
│   │   ├── rpc-client.ts       # RPC Client
│   │   └── websocket.ts        # WebSocket Wrapper
│   │
│   ├── assets/                 # Static Assets
│   │   └── styles/
│   │       └── main.css        # Global Styles
│   │
│   ├── components/             # Components
│   │   ├── common/             # Common Components
│   │   ├── layout/             # Layout Components
│   │   └── office/             # Office Scene Components
│   │
│   ├── composables/            # Composables
│   │   ├── useEventStream.ts   # Event Stream
│   │   ├── useResizable.ts     # Resize Handling
│   │   └── useTheme.ts         # Theme Management
│   │
│   ├── i18n/                   # Internationalization
│   │   ├── messages/
│   │   │   ├── zh-CN.ts        # Chinese
│   │   │   └── en-US.ts        # English
│   │   └── index.ts
│   │
│   ├── layouts/                # Layouts
│   │   └── DefaultLayout.vue
│   │
│   ├── router/                 # Router
│   │   ├── index.ts
│   │   └── routes.ts
│   │
│   ├── stores/                 # Pinia State Management
│   │   ├── agent.ts            # Agent
│   │   ├── auth.ts             # Authentication
│   │   ├── channel.ts          # Channel
│   │   ├── chat.ts             # Chat
│   │   ├── config.ts           # Configuration
│   │   ├── cron.ts             # Scheduled Tasks
│   │   ├── memory.ts           # Memory
│   │   ├── model.ts            # Model
│   │   ├── session.ts          # Session
│   │   ├── skill.ts            # Skill
│   │   ├── terminal.ts         # Terminal
│   │   ├── theme.ts            # Theme
│   │   ├── websocket.ts        # WebSocket
│   │   └── ...
│   │
│   ├── utils/                  # Utilities
│   │   ├── channel-config.ts
│   │   ├── format.ts
│   │   ├── markdown.ts
│   │   └── secret-mask.ts
│   │
│   ├── views/                  # Page Views
│   │   ├── agents/             # Multi-Agent
│   │   ├── channels/           # Channel Management
│   │   ├── chat/               # Online Chat
│   │   ├── cron/               # Scheduled Tasks
│   │   ├── memory/             # Memory Management
│   │   ├── models/             # Model Management
│   │   ├── sessions/           # Session Management
│   │   ├── skills/             # Skill Management
│   │   ├── system/             # System Monitoring
│   │   ├── terminal/           # Remote Terminal
│   │   ├── remote-desktop/     # Remote Desktop
│   │   ├── files/              # File Browser
│   │   ├── office/             # Agent Workshop
│   │   ├── myworld/            # Virtual Company
│   │   ├── monitor/            # Operations Center
│   │   ├── settings/           # System Settings
│   │   ├── Dashboard.vue       # Dashboard
│   │   └── Login.vue           # Login Page
│   │
│   ├── App.vue                 # Root Component
│   ├── main.ts                 # Entry File
│   └── env.d.ts                # Environment Type Declarations
│
├── server/                     # Backend Services
│   ├── index.js                # Server Entry
│   ├── gateway.js              # Gateway Connection
│   └── database.js             # Database Operations
│
├── public/                     # Public Static Assets
├── dist/                       # Build Output
├── data/                       # Data Storage
│
├── vite.config.ts              # Vite Configuration
├── tsconfig.json               # TypeScript Configuration
├── package.json                # Project Configuration
├── .env.example                # Environment Variables Example
└── .env                        # Local Environment Variables (copied from .env.example)
```

***

## Development Guide

### Code Style

- Use Vue 3 Composition API + `<script setup lang="ts">`
- Follow 2-space indentation, single quotes, trailing commas, no semicolons
- Use `@/` alias for `src` path imports

### Naming Conventions

| Type        | Convention     | Example                |
| ----------- | -------------- | ---------------------- |
| Components  | PascalCase.vue | `ConnectionStatus.vue` |
| Route Pages | \*Page.vue     | `SessionsPage.vue`     |
| Store       | camelCase.ts   | `session.ts`           |
| Composable  | use\*.ts       | `useTheme.ts`          |

### Build Verification

Before submitting, ensure:

```bash
npm run build
```

Build passes with no type errors.

### Environment Variables

First copy the example file, then fill in according to your local environment:

```bash
cp .env.example .env
```

Then configure in `.env` file:

```env
VITE_APP_TITLE=OpenClaw Admin
OPENCLAW_WS_URL=ws://localhost:18789
OPENCLAW_AUTH_TOKEN=
OPENCLAW_AUTH_PASSWORD=      # Gateway password, either one with Token is enough
PORT=3001
DEV_PORT=3000
DEV_FRONTEND_URL=http://localhost:3000
AUTH_USERNAME=
AUTH_PASSWORD=
MEDIA_DIR=
# OPENCLAW_HOME=/path/to/.openclaw
```

***

## API Reference

### WebSocket RPC Methods

The project communicates with OpenClaw Gateway via WebSocket, supporting the following RPC methods:

#### Configuration Management

- `config.get` - Get configuration
- `config.patch` - Update configuration
- `config.set` - Set configuration
- `config.apply` - Apply configuration

#### Session Management

- `sessions.list` - List sessions
- `sessions.get` - Get session details
- `sessions.reset` - Reset session
- `sessions.delete` - Delete session
- `sessions.spawn` - Create session
- `sessions.history` - Get history
- `sessions.usage` - Get usage statistics

#### Channel Management

- `channels.status` - Get channel status
- `channel.auth` - Channel authentication
- `channel.pair` - Channel pairing

#### Agent Management

- `agents.list` - List agents
- `agents.create` - Create agent
- `agents.update` - Update agent
- `agents.delete` - Delete agent
- `agents.files.list` - List files
- `agents.files.get` - Get file
- `agents.files.set` - Set file

#### Model Management

- `models.list` - List models

#### Scheduled Tasks

- `cron.list` - List tasks
- `cron.add` - Add task
- `cron.update` - Update task
- `cron.delete` - Delete task
- `cron.run` - Execute task

#### System Monitoring

- `health` - Health check
- `status` - Status query
- `system-presence` - Instance status
- `logs.tail` - View logs

***

## Security Notes

- ⚠️ **Never commit** real Gateway tokens, credentials, or other sensitive information
- Credential fields use masked display, plain text is never echoed
- API Keys are only submitted when a new value is entered, otherwise the original value is kept

***

## License

[MIT License](LICENSE)

***

## Contributing

Issues and Pull Requests are welcome!

**GitHub Repository**: <https://github.com/itq5/OpenClaw-Admin>

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

***

## Contact

### Author Email

📧 <root@itq5.com>

### WeChat Group

Welcome to join our WeChat group for latest updates and technical support:

![WeChat Group](docs/images/微信群.png)

***

<p align="center">
  Made with ❤️ by <a href="https://github.com/itq5/OpenClaw-Admin">OpenClaw Admin</a> Team
</p>
