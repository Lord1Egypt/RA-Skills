# Installation Guide

## Prerequisites

- **OpenClaw v1.0+** installed and running
- **Python 3.8+** environment
- **Approximately 100MB** disk space

## Installation Methods

### Method 1: Git Clone (Recommended)
```bash
# Clone the repository
git clone https://github.com/JamieYang9996/Heartbeat-Memories.git

# Copy to OpenClaw skills directory
cp -r Heartbeat-Memories ~/.openclaw/skills/heartbeat-memories

# Initialize the system
cd ~/.openclaw/skills/heartbeat-memories && python3 scripts/hbm_init.py
```

### Method 2: Manual Installation
1. Download the skill folder
2. Place it in your OpenClaw skills directory: `~/.openclaw/skills/`
3. Run initialization: `python3 scripts/hbm_init.py`

### Method 3: Via ClawHub (If Published)
```bash
openclaw skill install heartbeat-memories
```

## Initialization

After installation, run the initialization script:

```bash
cd ~/.openclaw/skills/heartbeat-memories
python3 scripts/hbm_init.py
```

The initialization script will:
1. Check Python dependencies
2. Create memory directory structure
3. Generate configuration files
4. Run diagnostic checks

## Configuration

### Basic Configuration
Edit the configuration file: `config/hbm_config.json`

Key configuration options:
- `memory_system.enabled`: Enable/disable memory recording
- `semantic_search.enabled`: Enable/disable semantic search
- `heartbeat_recall.enabled`: Enable/disable heartbeat recall
- `rag_system.enabled`: Enable/disable RAG system (default: OFF)

### Memory Location
By default, memories are stored in the `memory/` directory within the skill folder.

You can customize the memory location by setting the `memory_path` in configuration.

## Verification

To verify the installation is working:

```bash
# Run diagnostic check
python3 scripts/hbm_init.py --check

# Test semantic search
python3 scripts/local_memory_system_v2.py --search "test query"

# Check system status
python3 scripts/rag_system.py --config config/hbm_config.json
```

## Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError" for chromadb/sentence-transformers**
```bash
# Install missing dependencies
pip install chromadb sentence-transformers faiss-cpu
```

**Issue: Permission denied when accessing files**
```bash
# Check file permissions
chmod -R 755 ~/.openclaw/skills/heartbeat-memories
```

**Issue: Vector database initialization fails**
```bash
# Delete and recreate vector database
rm -rf memory/vector_db
python3 scripts/hbm_init.py
```

**Issue: Configuration file not found**
```bash
# Copy template configuration
cp config/hbm_config_template.json config/hbm_config.json
```

## Uninstallation

To completely remove Heartbeat-Memories:

```bash
# 1. Remove the skill directory
rm -rf ~/.openclaw/skills/heartbeat-memories

# 2. Remove any memory data (optional, backup first)
rm -rf ~/.openclaw/workspace/memory  # If you used default location

# 3. Remove Python packages (optional)
pip uninstall chromadb sentence-transformers faiss-cpu
```

## Next Steps

After successful installation:
1. Restart OpenClaw Gateway if needed
2. Test with trigger words in OpenClaw conversation
3. Review configuration for customization
4. Check `README.md` for advanced features