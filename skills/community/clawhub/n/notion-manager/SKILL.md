---
name: notion
description: Production-ready Notion API client for SaaS workflows. Create/read/update pages, query data sources, append blocks.
author: tomas-mikula
web: https://FrontendAccelerator.com
env:
  - NOTION_API_KEY
primary-credential: NOTION_API_KEY
---

## Description
Execute Notion API operations with automatic version header and structured outputs.

## Usage
{"auth": {"notionApiKey": "secret_..."}, "input": {"operation": "queryDataSource", "params": {"dataSourceId": "abc123"}}}

Operations: search, getPage, queryDataSource, createPage, updatePage, appendBlocks, createDataSource

## Input schema
{"type": "object", "properties": {"operation": {"type": "string", "enum": ["search","getPage","queryDataSource","createPage","updatePage","appendBlocks","createDataSource"]}, "params": {"type": "object"}}, "required": ["operation"]}

## Output schema
{"type": "object", "properties": {"status": {"type": "string", "enum": ["success","error"]}, "data": {}, "meta": {}, "error_type": {"type": "string"}, "http_status": {"type": "integer"}}, "required": ["status"]}

## Environment variables
NOTION_API_KEY: secret_ or ntn_ key from notion.so/my-integrations
