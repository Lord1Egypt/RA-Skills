# TOOLS.md - Technical References (Komi - CTO Agent)

## API Keys & External Services

### Gemini API (for background generation)
- **Usage**: Generating isometric pixel art office backgrounds
- **Status**: Configured and tested
- **Model**: gemini-2.5-flash (Nano Banana Pro)
- **Endpoint**: https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent

### PixelLab API (for asset generation)
- **Usage**: Generating character sprites and office furniture/assets
- **Status**: To be integrated
- **Documentation**: Needs to be reviewed

### Office Communication
- **Internal Agent Communication**: Shared memory files and structured updates
- **External Reporting**: Regular status updates to Komi (任務總管)
- **User Support**: Coordination with EDN agent for end-user assistance

## Development Tools

### Rendering Engine
- **PixiJS**: 2D rendering engine for isometric view
- **Version**: Latest stable
- **Documentation**: https://pixijs.download/release/docs/index.html
- **Usage**: Main viewport rendering for KCC Office v2

### Asset Management
- **File Naming Convention**: 
  - Backgrounds: `office_bg_[description].webp`
  - Characters: `[role]_[pose]_[direction].webp`
  - UI Elements: `ui_[element]_[state].webp`
- **Optimization**: WebP format for balance of quality and file size
- **Sprite Sheets**: Used for animated elements when needed

### Project Structure
```
/kcc-office-ai-agents/
├── agents/                 # Individual agent workspaces
│   ├── komi/              # CTO agent workspace
│   ├── ceo/               # CEO agent workspace
│   ├── cfo/               # CFO agent workspace
│   ├── cto/               # (This agent - redundant naming, consider refactor)
│   ├── coo/               # COO agent workspace
│   └── edn/               # EDN agent workspace
├── scripts/               # Automation and utility scripts
├── memory/                # Shared or global memory (if applicable)
├── assets/                # Generated assets (backgrounds, characters, etc.)
├── docs/                  # Technical documentation
└── configs/               # Configuration files
```

## Technical Standards

### Code Quality
- **JavaScript/TypeScript**: ES2020+ features where supported
- **Code Formatting**: Prettier with 2-space indentation
- **Linting**: ESLint with recommended rules
- **Comments**: JSDoc for public APIs, inline comments for complex logic

### Git Practices
- **Branch Naming**: `feature/`, `bugfix/`, `refactor/`, `docs/`
- **Commit Messages**: Conventional Commits format
- **PR Template**: Include context, testing, and checklist
- **Code Review**: Minimum 1 approving review for merge to main

### Testing Strategy
- **Unit Tests**: Jest or Vitest for individual functions
- **Integration Tests**: Test agent interactions and workflows
- **E2E Tests**: Simulate user journeys through the office
- **Performance Tests**: Benchmark critical paths and rendering

## Deployment & Operations

### Environment Variables
- `NODE_ENV`: development | staging | production
- `GEMINI_API_KEY`: For background generation
- `PIXELLAB_API_KEY`: For asset generation (when available)
- `PORT`: Server port (default: 19000 for office UI)
- `LOG_LEVEL`: error | warn | info | debug

### Monitoring & Alerting
- **Health Checks**: `/health` endpoint returning JSON status
- **Metrics**: Basic request/response timing and error rates
- **Logs**: Structured logging for debugging and audit trails
- **Alerts**: Threshold-based notifications for critical metrics

### Backup & Recovery
- **Regular Backups**: Daily snapshots of critical data
- **Version Control**: Git for code and configuration
- **Disaster Recovery**: Documented procedures for service restoration
- **Data Integrity**: Checksums for critical files when applicable

## Troubleshooting Guide

### Common Issues
- **Context Loss**: Check SESSION-STATE.md and working-buffer.md for recovery
- **Communication Failures**: Verify shared file permissions and paths
- **Performance Degradation**: Look for memory leaks or inefficient loops
- **Integration Problems**: Verify API keys and endpoint availability

### Debugging Approaches
- **WAL Protocol**: Always check SESSION-STATE.md first for recent context
- **Working Buffer**: Review memory/working-buffer.md for recent exchanges
- **Log Tracing**: Follow error logs and debug output systematically
- **Isolation**: Test components individually before integration

## References

### Internal
- KCC-OFFICE.md - Project overview and status
- PROACTIVE-AGENT-SUMMARY.md - Key patterns from proactive-agent skill
- SELF-IMPROVEMENT-SUMMARY.md - Key patterns from self-improving-agent skill

### External
- PixiJS Documentation: https://pixijs.download/release/docs/index.html
- Gemini API Docs: https://ai.google.dev/gemini-api/docs
- Web Optimization: https://web.dev/articles/image-optimization

---
*此檔案由 Komi (CTO) 維護，用於追蹤技術參考和工具資訊。*