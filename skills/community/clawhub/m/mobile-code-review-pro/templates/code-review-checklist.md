# Mobile Code Review Checklist

## Quick Scan (30 minutes)

### Architecture
- [ ] Code organized by feature (not layer)
- [ ] Clear separation of concerns
- [ ] Dependency injection used appropriately
- [ ] State management consistent

### Performance
- [ ] App startup < 3 seconds
- [ ] Smooth 60 FPS scrolling
- [ ] No obvious memory leaks
- [ ] Network calls optimized

### Security
- [ ] No hardcoded secrets
- [ ] API keys in secure storage
- [ ] HTTPS enforced
- [ ] User data encrypted

### Code Quality
- [ ] Consistent naming conventions
- [ ] Functions < 50 lines
- [ ] No god classes
- [ ] Tests exist for critical paths

---

## Deep Dive (1-2 days)

### iOS Specific

**Memory Management:**
- [ ] ARC used correctly
- [ ] No retain cycles
- [ ] Weak references where needed
- [ ] Deinit properly implemented

**UI Performance:**
- [ ] Auto Layout optimized
- [ ] View hierarchy reasonable
- [ ] Image loading efficient
- [ ] Main thread free of blocking

**Battery:**
- [ ] Background tasks minimal
- [ ] Location updates optimized
- [ ] Network batching used
- [ ] Push notifications efficient

**Swift Best Practices:**
- [ ] Optionals handled safely
- [ ] Guard statements used
- [ ] Protocol-oriented design
- [ ] Extension organization logical

### Android Specific

**Memory:**
- [ ] No context leaks
- [ ] Bitmap handling correct
- [ ] Cursor management proper
- [ ] WeakReferences where needed

**Performance:**
- [ ] View hierarchy flat
- [ ] RecyclerView optimized
- [ ] Background threads used
- [ ] Database queries indexed

**Battery:**
- [ ] WorkManager used correctly
- [ ] JobScheduler optimized
- [ ] Doze mode compatible
- [ ] Network efficient

**Kotlin Best Practices:**
- [ ] Null safety utilized
- [ ] Coroutines used properly
- [ ] Extension functions logical
- [ ] Data classes used

### React Native Specific

**Bridge:**
- [ ] Native modules efficient
- [ ] Serialization optimized
- [ ] Batched bridge calls
- [ ] TurboModules considered

**Bundle:**
- [ ] Bundle size < 50MB
- [ ] Lazy loading implemented
- [ ] Dead code removed
- [ ] Hermes enabled

**Performance:**
- [ ] FlatList optimized
- [ ] Images cached
- [ ] Animations native-driven
- [ ] JS thread not blocked

---

## Security Deep Dive

### Data Protection
- [ ] Sensitive data in Keychain/Keystore
- [ ] Database encrypted (SQLCipher)
- [ ] Logs don't contain secrets
- [ ] User data cleared on logout

### Network Security
- [ ] Certificate pinning implemented
- [ ] SSL/TLS enforced
- [ ] API tokens refreshed securely
- [ ] Man-in-the-middle prevented

### Authentication
- [ ] Biometric storage secure
- [ ] Session management proper
- [ ] OAuth implemented correctly
- [ ] Token storage secure

### Third-Party Libraries
- [ ] Dependencies up-to-date
- [ ] No known vulnerabilities
- [ ] Minimal dependency count
- [ ] License compliance checked

---

## Performance Benchmarks

### Startup Time
| App Size | Target | Warning | Critical |
|----------|--------|---------|----------|
| < 50 screens | < 1.5s | 1.5-2.5s | > 2.5s |
| 50-200 screens | < 2.0s | 2.0-3.0s | > 3.0s |
| > 200 screens | < 2.5s | 2.5-4.0s | > 4.0s |

### Memory Usage
| App Type | Target | Warning | Critical |
|----------|--------|---------|----------|
| Simple | < 100MB | 100-150MB | > 150MB |
| Medium | < 150MB | 150-200MB | > 200MB |
| Complex | < 200MB | 200-300MB | > 300MB |

### Crash Rate
| Rating | Crash-Free % |
|--------|--------------|
| Excellent | > 99.9% |
| Good | 99.5-99.9% |
| Acceptable | 99.0-99.5% |
| Poor | < 99.0% |

---

## Severity Ratings

### Critical (Fix Immediately)
- Security vulnerabilities
- Data loss risks
- App crashes
- Performance blocking UX

### High (Fix This Sprint)
- Memory leaks
- Battery drain issues
- Major performance issues
- Significant tech debt

### Medium (Fix Next Sprint)
- Code quality issues
- Minor performance optimization
- Inconsistent patterns
- Missing tests

### Low (Backlog)
- Nice-to-have improvements
- Minor refactoring
- Documentation gaps
- Style inconsistencies

---

## Common Issues & Quick Fixes

### 1. Slow Startup
**Issue:** App takes > 3 seconds to launch
**Quick Fix:**
- Lazy load non-critical features
- Optimize splash screen
- Reduce initial network calls
- Profile with Instruments/Profiler

### 2. Memory Leaks
**Issue:** Memory grows over time
**Quick Fix:**
- Check for retain cycles (iOS)
- Use LeakCanary (Android)
- Review listener cleanup
- Check bitmap disposal

### 3. Janky Scrolling
**Issue:** Frames drop during scroll
**Quick Fix:**
- Optimize cell complexity
- Use recycling properly
- Reduce shadow effects
- Enable hardware acceleration

### 4. Large Bundle Size
**Issue:** App > 100MB download
**Quick Fix:**
- Compress images
- Remove unused assets
- Enable app bundles (Android)
- Lazy load resources

---

## Reporting Template

### Issue Format
```
**Issue:** [Short description]
**Severity:** [Critical/High/Medium/Low]
**Location:** [File:Line]
**Impact:** [User/business impact]
**Root Cause:** [Why it happens]
**Solution:** [How to fix]
**Effort:** [Hours/Days]
```

### Example
```
**Issue:** Memory leak in UserProfileViewController
**Severity:** High
**Location:** UserProfileViewController.swift:45
**Impact:** App crashes after 30 minutes of use
**Root Cause:** Retain cycle in closure without [weak self]
**Solution:** Add [weak self] to closure capture list
**Effort:** 1 hour
```

---

**Checklist version:** 1.0
**Last updated:** Feb 2026
**Based on:** MileIQ codebase (2M+ lines reviewed)
