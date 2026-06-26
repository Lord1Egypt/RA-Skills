# Memphis Cognitive Engine Skill

**Decision-first AI memory for OpenClaw**

---

## 🎯 Co to jest?

To **META-PACKAGE** dla OpenClaw który integruje **Memphis Cognitive Engine** - kompletny system pamięci AI.

**⚠️ WAŻNE:** Skill to tylko dokumentacja. Memphis CLI musi być zainstalowany osobno.

---

## 🚀 Szybki Start (5 min)

### Step 1: Install Memphis CLI (4 min)

```bash
# Clone + build
git clone https://github.com/elathoxu-crypto/memphis.git ~/memphis
cd ~/memphis
npm install
npm run build

# Global command
npm link

# Or use npm script:
# npm run install-global
```

### Step 2: Install Skill (1 min)

```bash
clawhub install memphis-cognitive
```

### Step 3: Initialize (30 sec)

```bash
memphis init
```

✅ **Gotowe!** Memphis działa! 🎉

---

## 💡 Co jest w skillu?

To **META-PACKAGE** który zawiera:
- ✅ **SKILL.md** - Instrukcje dla agenta (523 linii)
- ✅ **README.md** - Dokumentacja (186 linii)
- ✅ **memphis-wrapper.sh** - Wrapper script

**NIE zawiera:**
- ❌ Memphis CLI binary
- ❌ dist/ folder
- ❌ node_modules/

---

## 🔧 Dlaczego osobna instalacja?

### Architektura:

```
ClawHub skill (META-PACKAGE)
├── SKILL.md (dokumentacja)
└── README.md (quick start)

Memphis CLI (z GitHub)
├── dist/cli/index.js (binary)
└── node_modules/ (dependencies)
```

**Dlaczego?**
- ClawHub skills są lightweight (tylko dokumentacja)
- Memphis CLI wymaga buildu (TypeScript → JavaScript)
- Lepsza kontrola wersji

---

## 📋 Pełna instalacja (krok po kroku)

### 1. Node.js (wymagany)

```bash
# Install Node.js 20 LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Verify
node --version
```

### 2. Git (wymagany)

```bash
sudo apt install -y git
git --version
```

### 3. Memphis CLI

```bash
# Option 1: One-liner (RECOMMENDED)
curl -fsSL https://raw.githubusercontent.com/elathoxu-crypto/memphis/main/install.sh | bash

# Option 2: Manual
git clone https://github.com/elathoxu-crypto/memphis.git ~/memphis
cd ~/memphis && npm install && npm run build
npm link

# Option 3: From npm (when published)
npm install -g @elathoxu-crypto/memphis
```

### 4. ClawHub skill

```bash
clawhub install memphis-cognitive
```

### 5. Ollama (optional)

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull nomic-embed-text
```

### 6. OpenClaw (optional)

```bash
npm install -g openclaw
openclaw gateway start
```

---

## 🧪 Test

```bash
# 1. Check CLI
memphis --version

# 2. Initialize
memphis init

# 3. Status
memphis status

# 4. Test commands
memphis journal "Test" --tags test
memphis ask "Test?"
memphis decide "Test" "A" -r "Testing"
```

---

## 🎯 Use Cases

### Developer:
```bash
memphis decide "Use TypeScript" "TypeScript" -r "Type safety"
memphis infer --since 7  # Detect from git
memphis predict --learn  # Learn patterns
```

### Entrepreneur:
```bash
memphis decide "Pricing" "Tiered" -r "Free tier drives adoption"
memphis journal "Client meeting notes"
memphis reflect --weekly
```

### Team Lead:
```bash
memphis share-sync --push  # Multi-agent sync
memphis graph build        # Knowledge graph
memphis trade create ...   # Share with team
```

---

## 🚀 Advanced Features

### All 100% working (17/17 commands):

**Core:**
- journal, ask, decide, recall, reflect

**Advanced:**
- tui (dashboard)
- graph (knowledge graph)
- trade (multi-agent protocol)
- share-sync (multi-agent sync)
- decisions list

**Cognitive Models:**
- Model A (conscious)
- Model B (inferred)
- Model C (predictive)

---

## ⚠️ Troubleshooting

### `memphis: command not found`

**Problem:** Skill zainstalowany, ale CLI brakuje.

**Solution:**
```bash
cd ~/memphis
npm link
```

### `Cannot find module`

**Problem:** Build nie został wykonany.

**Solution:**
```bash
cd ~/memphis
npm install
npm run build
```

### `Skill not working`

**Problem:** Agent nie widzi komend.

**Solution:**
```bash
# Check skill location
ls ~/.openclaw/workspace/skills/memphis-cognitive/

# Restart OpenClaw
openclaw gateway restart
```

---

## 📊 Co masz po instalacji

```
~/
 ├── memphis/                    # Memphis CLI
 │   ├── dist/cli/index.js       # Binary
 │   └── package.json
 │
 ├── .memphis/                   # Data
 │   ├── chains/
 │   └── config.yaml
 │
 └── .openclaw/workspace/skills/
     └── memphis-cognitive/      # Skill (META-PACKAGE)
         ├── SKILL.md            # Instrukcje
         └── README.md           # Docs
```

---

## 🔗 Links

- **Memphis CLI:** https://github.com/elathoxu-crypto/memphis
- **ClawHub Skill:** https://clawhub.com/skill/memphis-cognitive
- **Discord:** https://discord.gg/clawd
- **Docs:** https://github.com/elathoxu-crypto/memphis/tree/master/docs

---

## 🇵🇱 Polish Support

Memphis wspiera polskie keywords:
- `zdecydowałem, wybrałem, postanowiłem`
- `klient, faktura, spotkanie`
- `decyzja, wybór`

---

## 📝 Summary

**To skill to:**
- ✅ META-PACKAGE (dokumentacja)
- ✅ Instrukcje dla OpenClaw agenta
- ✅ Quick start guide

**Wymaga:**
- ⚠️ Memphis CLI z GitHub
- ⚠️ Node.js 18+
- ⚠️ Git

**Daje:**
- ✅ 17 komend (100% working)
- ✅ 3 modele kognitywne
- ✅ Advanced features
- ✅ Multi-agent network

---

**Created by:** Elathoxu Abbylan  
**License:** MIT  
**Version:** 3.6.3  
**Status:** ✅ Production Ready  
**Updated:** 2026-03-04 20:05 CET

**Questions?** Join Discord or check docs!
