---
name: java-maven-common
description: Common input handling for Java Maven project review workflows. Use when a Java Maven project arrives as a ZIP archive or a GitLab repository URL and you need to unpack, clone, normalize the project root, and identify Maven modules before deeper review or analysis.
---

# Java Maven Common

Use this skill as the shared input layer for Java Maven review work.

## Purpose

This skill handles the common project-ingest steps used by other Java Maven skills:
- ZIP unpack
- GitLab clone after SSH authorization
- project root normalization
- Maven root/module identification

## Supported input
- Java Maven ZIP archive
- GitLab repository URL

## Standard workflow

### ZIP input
1. Put archive into `temp/`
2. Unpack into a dedicated work directory under `temp/`
3. Normalize root directory
4. Detect Maven modules by scanning `pom.xml`

### GitLab input
1. Confirm SSH authorization has been granted by the user
2. Clone repository into a dedicated work directory under `temp/`
3. Normalize root directory
4. Detect Maven modules by scanning `pom.xml`

## Output

Generate a JSON summary that includes at least:
- input mode
- normalized root path
- project name
- module list
- module count
- whether scan is limited

## Bundled resources
- `scripts/prepare_java_maven_project.py`

## Instruction scope

This skill does not produce the final business report by itself. It prepares the project input for downstream skills.
