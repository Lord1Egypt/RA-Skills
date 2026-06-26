# Trust Model

## Dependency Trust Relationship

This skill (`ios-self-improve`) has one mandatory dependency: `developer-self-improve-core`.

### Why Trust This Dependency?

**1. Same Author**
- Both skills are authored by: lijiujiu
- Same development team, same security standards

**2. Open Source**
- Both skills are open source (MIT License)
- Code can be audited by anyone
- No hidden or obfuscated logic

**3. Declared Dependency**
- Dependency is explicitly declared in `.clawhub.json`
- Not a hidden or runtime-only dependency
- Users can review before installing

**4. Read-Only Access**
- This skill only READS configuration from `developer-self-improve-core`
- No modifications to the dependency's files
- No execution of external code

**5. Same Security Standards**
- Both skills follow the same security principles:
  - No automatic memory modification
  - Human-in-the-loop for all changes
  - All operations are logged
  - Platform isolation

### What Happens If Dependency Is Missing?

If `developer-self-improve-core` is not installed:

1. **Installation Warning**
   - ClawHub will warn users about the missing dependency
   - Users can choose to install both or cancel

2. **Runtime Behavior**
   - This skill will check for the dependency
   - If missing, it will display a helpful error message
   - No crashes or undefined behavior

3. **Graceful Degradation**
   - Platform checks will use default values
   - Rule generation will be skipped with a clear message
   - Users are guided to install the dependency

### Security Boundaries

**This skill CAN:**
- ✅ Read configuration from `developer-self-improve-core/config/config.yaml`
- ✅ Call `developer-self-improve-core` scripts for rule generation
- ✅ Check platform settings

**This skill CANNOT:**
- ❌ Modify `developer-self-improve-core` files
- ❌ Execute arbitrary code from the dependency
- ❌ Access system-level resources
- ❌ Make external network calls

### User Control

Users have full control:

1. **Before Installation**
   - Review `.clawhub.json` to see dependencies
   - Read `DEPENDENCY_EXPLANATION.md` for details
   - Read `TRUST_MODEL.md` (this file) for trust information

2. **After Installation**
   - Can disable this skill at any time
   - Can uninstall without affecting the dependency
   - Can review all operations in logs

### Comparison

| Aspect | This Skill | Dependency |
|--------|------------|------------|
| **Author** | lijiujiu | lijiujiu |
| **License** | MIT | MIT |
| **Type** | Platform extension | Core engine |
| **Operations** | Read-only | Read/Write (with approval) |
| **Network** | None | None |
| **System** | None | None |

### Conclusion

The dependency on `developer-self-improve-core` is:
- ✅ Explicitly declared
- ✅ Same author and standards
- ✅ Read-only access
- ✅ Open source and auditable
- ✅ Safe for use

Users should install `developer-self-improve-core` first, then this skill.
