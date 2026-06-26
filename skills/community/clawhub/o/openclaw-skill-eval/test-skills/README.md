# Test Skills

Bundled skills for testing skill-eval functionality.

## fake-tool

A fake skill that queries a non-existent "Zephyr API". Used to test trigger rate detection because:

1. **Model doesn't know Zephyr** — forces the model to read SKILL.md
2. **Has obscure commands** — model can't guess the syntax
3. **Safe to run** — commands will fail gracefully (CLI not installed)

### Setup (Required Before Testing)

1. **Copy to your skills directory**:
   ```bash
   cp -r test-skills/fake-tool ~/.openclaw/workspace/skills/
   ```

2. **Verify it's in extraDirs** (check `~/.openclaw/openclaw.json`):
   ```json
   "skills": {
     "load": {
       "extraDirs": [
         "~/.openclaw/workspace/skills"
       ]
     }
   }
   ```

3. **Restart OpenClaw gateway**:
   ```bash
   openclaw gateway restart
   ```

4. **Run the test**:
   ```
   evaluate fake-tool trigger
   ```

### Expected Behavior

When you ask "Check the Zephyr server status", the agent should:
1. ✅ Read `fake-tool/SKILL.md` (this is what we're testing)
2. Try to run `zephyr status --format json`
3. Fail gracefully (CLI not installed)

The trigger is **successful** if step 1 happens — the agent correctly identified and read the skill.
