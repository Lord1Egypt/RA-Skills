# Makefile — idle-ping 開發/測試入口（專業標準）
# 用法：
#   make lint   # ShellCheck + 語法檢查
#   make test   # BATS 測試
#   make check  # 全部（lint + test）= 本地模擬 CI
#   make ci     # 同 check

SHELL := /bin/bash

# 本地可能未裝 bats（CI 會 apt install）；fallback 去 /tmp/bats-core
BATS := $(shell command -v bats 2>/dev/null || echo /tmp/bats-core/bin/bats)

.PHONY: lint test check ci

lint:
	@echo "==> ShellCheck"
	shellcheck scripts/*.sh install.sh
	@echo "==> Syntax check"
	bash -n scripts/*.sh install.sh
	python3 -m py_compile scripts/share-queue.py scripts/semantic-patrol.py scripts/topic-factory.py
	@echo "✅ lint 通過"

test:
	@echo "==> BATS 測試"
	"$(BATS)" tests/
	@echo "✅ test 通過"

check: lint test
	@echo "🎉 全部檢查通過（同 GitHub CI 一樣）"

ci: check
