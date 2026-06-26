---
name: linkedcareer
displayName: LinkedCareer
description: Career management and resume generation skill
metadata:
  openclaw:
    type: runtime
    requires:
      bins: ["node"]
    install: npm install --production
    commands:
      - name: init
        description: Initialize career profile
      - name: deepdive
        description: Extract career highlights
      - name: record
        description: Record work growth
      - name: resume
        description: Generate professional resume
      - name: import
        description: Import existing resume
---
# LinkedCareer
## Features
- Guided onboarding to build career profile
- Deep dive analysis to find hidden achievements
- Regular growth tracking (daily/weekly/monthly)
- Multiple professional resume templates
- JD matching to optimize resume for roles
- Runtime: No network requests, all data stored locally
- Installation: Requires network to download docx from npm
## Quick Start
```
/linkedcareer init
/linkedcareer deepdive
/linkedcareer record
/linkedcareer resume
```
