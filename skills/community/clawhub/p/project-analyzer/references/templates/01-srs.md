# {{PROJECT_NAME}} - Software Requirements Specification (SRS)

## Document Info

| Item | Content |
|------|---------|
| Project Name | {{PROJECT_NAME}} |
| Version | {{VERSION}} |
| Author | {{AUTHOR}} |
| Date | {{DATE}} |

---

## 1. Introduction

### 1.1 Purpose

This document describes the software requirements specification for **{{PROJECT_NAME}}**.

### 1.2 Scope

Core features provided by this project:

{{FEATURE_OVERVIEW}}

### 1.3 Definitions

| Term | Definition |
|------|-----------|
| API | Application Programming Interface |
| SDK | Software Development Kit |
| SSO | Single Sign-On |

---

## 2. Overall Description

### 2.1 Product Background

{{PROJECT_NAME}} is an enterprise application based on {{TECH_STACK}}.

### 2.2 Technology Architecture

| Layer | Technology | Description |
|-------|------------|-------------|
| Framework | {{FRAMEWORK}} | Core framework |
| Database | {{DATABASE}} | Data storage |
| Cache | {{CACHE}} | Cache acceleration |
| MQ | {{MQ}} | Async processing |

### 2.3 Module Structure

{{MODULE_OVERVIEW}}

---

## 3. Functional Requirements

### 3.1 Core Modules

{{FUNCTIONAL_MODULES}}

### 3.2 Feature List

| Feature ID | Name | Priority | Description |
|------------|------|----------|-------------|
{{FEATURE_LIST}}

---

## 4. Non-Functional Requirements

### 4.1 Performance

| Metric | Requirement | Description |
|--------|------------|-------------|
| API Response | P99 < 200ms | Under normal load |
| Concurrency | 500+ QPS | Per instance |
| Throughput | 1000 req/s | Max throughput |

### 4.2 Security

| Requirement | Description |
|------------|-------------|
| Authentication | JWT Token |
| Authorization | RBAC |
| Encryption | HTTPS |

### 4.3 Availability

| Metric | Requirement |
|--------|-------------|
| Availability | 99.9% |
| Recovery | < 5 min |
| Monitoring | Full链路监控 |

---

## 5. Interface Requirements

### 5.1 Overview

This project provides **{{API_COUNT}}** API interfaces.

### 5.2 Interface List

{{API_SUMMARY}}

---

*Version: {{VERSION}}*
*Last Updated: {{DATE}}*