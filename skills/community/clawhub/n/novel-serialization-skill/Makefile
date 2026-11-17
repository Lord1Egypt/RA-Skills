# Development entry points.
#
# Every target is a proxy to scripts/dev.py, which holds the actual commands.
# Keep it that way: two copies of the same flag list drift apart, and the one
# that drifts is always the one nobody runs.
#
# Windows has no make by default. Call the same thing directly:
#   python scripts/dev.py all

PYTHON ?= python
DEV := $(PYTHON) scripts/dev.py

.DEFAULT_GOAL := all
.PHONY: all test hygiene refs lint scaffold clean install

all: hygiene refs lint test

install:
	$(PYTHON) -m pip install -r requirements-dev.txt
	$(PYTHON) -m pre-commit install

test:
	$(DEV) test

hygiene:
	$(DEV) hygiene

refs:
	$(DEV) refs

lint:
	$(DEV) lint

ROOT_DIR ?= .

scaffold:
	@test -n "$(NAME)" || { echo "usage: make scaffold NAME=\"书名\" ROOT_DIR=../my-novel"; exit 2; }
	$(DEV) scaffold --name "$(NAME)" --root "$(ROOT_DIR)"

clean:
	rm -rf .workbuddy/.pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
