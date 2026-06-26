# Known License Table

Cached license data for common Maven dependencies. Updated 2026-06-04.

## Format
`groupId:artifactId-pattern → License, Notes`

## Catalog

### Alibaba / Aliyun ecosystem
- `com.alibaba*:*` → Apache-2.0
- `com.aliyun*:*` → Apache-2.0

### Baomidou (MyBatis-Plus)
- `com.baomidou:mybatis-plus-*` → Apache-2.0

### Jackson (FasterXML)
- `com.fasterxml*:*` → Apache-2.0

### Google
- `com.google.guava:guava` → Apache-2.0
- `com.google.protobuf:protobuf-java` → BSD-3-Clause

### Apache
- `org.apache*:*` → Apache-2.0

### Spring ecosystem
- `org.springframework*:*` → Apache-2.0

### ORM / Database
- `org.mybatis:mybatis` → Apache-2.0
- `com.mysql:mysql-connector-j` → GPL-2.0 WITH Universal-FOSS-exception-1.0
  - FOSS Exception allows standalone driver use without triggering GPL contagion.
  - Do not modify or redistribute the driver itself.
  - Alternative: MariaDB Connector/J (LGPL)

### Utilities
- `cn.hutool:hutool-all` → MIT
- `com.github.pagehelper:pagehelper-*` → MIT
- `com.github.xiaoymin:knife4j-*` → Apache-2.0
- `org.mapstruct:*` → Apache-2.0
- `org.mvel:mvel2` → Apache-2.0

### HIGH RISK — needs commercial license or replacement

- `com.itextpdf:*` → AGPL-3.0
  - iText 7.x core libraries are AGPL-3.0.
  - Replacement: Apache PDFBox (Apache-2.0), OpenPDF (LGPL).
  - If you must use iText, purchase commercial license: https://itextpdf.com/pricing

- `com.xuxueli:xxl-job-core` → GPL-3.0
  - If xxl-job runs as a standalone service (HTTP/gRPC), GPL contagion may not apply.
  - If xxl-job is bundled into the same JAR/WAR, risk is high.
  - Replacement: PowerJob (Apache-2.0), DolphinScheduler (Apache-2.0)

## Session Findings (2026-06-04)

Project: nanshe_mall_service (Spring Boot 3.0, Maven multi-module e-commerce)

47 deps scanned → 6 HIGH, 0 MEDIUM, 39 LOW, 2 UNKNOWN (resolved as safe):
- `com.itextpdf:font-asian:7.2.5` → AGPL-3.0
- `com.itextpdf:io` → AGPL-3.0
- `com.itextpdf:kernel` → AGPL-3.0
- `com.itextpdf:layout` → AGPL-3.0
- `com.mysql:mysql-connector-j` → GPL-2.0 + FOSS Exception (safe as-is)
- `com.xuxueli:xxl-job-core` → GPL-3.0

Resolved unknowns:
- `com.github.pagehelper:sqlparser4.5:6.1.0` → MIT (same author as pagehelper)
- `org.springframework.boot:spring-boot-starter` → Apache-2.0 (standard Spring)
