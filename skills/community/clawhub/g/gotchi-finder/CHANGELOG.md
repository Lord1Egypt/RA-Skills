# Changelog - gotchi-finder

## [1.2.1] - 2026-03-05

### Fixed
- `fetch-gotchi.js` now creates output directory before writing files (prevents ENOENT on direct usage).
- Added `equippedWearables` and `wearablesModifier` to JSON output for accurate wearable counts and display tooling.
- Improved shell script robustness in `find-gotchi.sh` and `show-gotchi.sh` (strict mode, argument guards, dependency checks).

### Changed
- Synced `package.json` + `VERSION` to `1.2.1`.

## [1.1.0] - 2026-02-22

### Changed - MAJOR UPDATE
- **BRS now shows TOTAL BRS (base + wearables modifiers)** 🔥
  - Uses `modifiedRarityScore` instead of `baseRarityScore`
  - Shows gotchi's true power level with all equipped gear
  - Wearables can change rarity tiers (e.g., MYTHICAL → GODLIKE)

### Added
- `baseBrs` field in JSON output (reference only)
- `modifiedTraits` - Shows traits with wearable bonuses
- Enhanced console output with BRS breakdown
- `BRS_POLICY.md` - Official BRS standard document

### Output Changes
**Before:**
```
⭐ BRS: 562
```

**After:**
```
⭐ Total BRS: 670 (Base: 562 + Wearables: +108)

👔 Modified Traits (with wearables):
   Energy: 9 (+3)
   Aggression: 100 (+7)
```

### Impact
- **Breaking Change:** BRS values increased for gotchis with wearables
- Cards and tools using this data will show higher BRS
- Some gotchis may jump rarity tiers

### Example
**SHAAMAAN (#22470):**
- Base: 562 (MYTHICAL)
- Wearables: +108
- **Total: 670 (GODLIKE!)** 🟢

---

## [1.0.3] - Previous
- Security fixes for ClawHub
- PNG conversion improvements

## [1.0.2] - Previous
- Initial ClawHub release
