#!/bin/bash
set -e

echo "🧪 Starting Blue/Green Deployment & Rollback Tests..."

TEMP_DIR=$(mktemp -d)
export HOME_MOCK="$TEMP_DIR"
SLUG=$(basename "$PWD")

SKILLS_DIR="$TEMP_DIR/.openclaw/skills"
RELEASES_DIR="$TEMP_DIR/.openclaw/.releases/$SLUG"

mkdir -p "$SKILLS_DIR/$SLUG"

# T1: Initial Deployment & Migration
echo "[T1] Testing Initial Deployment & Migration..."
echo "Simulating legacy directory..."
touch "$SKILLS_DIR/$SLUG/legacy_file.txt"

./deploy.sh > /dev/null

if [ -d "$SKILLS_DIR/$SLUG" ] && [ ! -L "$SKILLS_DIR/$SLUG" ]; then
    echo "❌ T1 FAILED: Legacy directory was not destroyed."
    exit 1
fi

if [ ! -L "$SKILLS_DIR/$SLUG" ]; then
    echo "❌ T1 FAILED: Symlink was not created."
    exit 1
fi

TARGET=$(readlink "$SKILLS_DIR/$SLUG")
if [[ ! "$TARGET" == *"$RELEASES_DIR/"* ]]; then
    echo "❌ T1 FAILED: Symlink points to incorrect location ($TARGET)."
    exit 1
fi

echo "✅ T1 PASSED."

# T2: Atomic Version Progression
echo "[T2] Testing Atomic Version Progression..."
FIRST_RELEASE=$(basename "$TARGET")
sleep 1
./deploy.sh > /dev/null

TARGET2=$(readlink "$SKILLS_DIR/$SLUG")
SECOND_RELEASE=$(basename "$TARGET2")

if [ "$FIRST_RELEASE" = "$SECOND_RELEASE" ]; then
    echo "❌ T2 FAILED: Symlink did not progress."
    exit 1
fi

COUNT=$(ls -d "$RELEASES_DIR"/*/ 2>/dev/null | grep -cE '/[0-9]{8}_[0-9]{6}/$')
if [ "$COUNT" -ne 2 ]; then
    echo "❌ T2 FAILED: Expected 2 releases, found $COUNT."
    exit 1
fi

echo "✅ T2 PASSED."

# T3: Instant Rollback
echo "[T3] Testing Instant Rollback..."
./scripts/rollback.sh > /dev/null

TARGET3=$(readlink "$SKILLS_DIR/$SLUG")
THIRD_RELEASE=$(basename "$TARGET3")

if [ "$THIRD_RELEASE" != "$FIRST_RELEASE" ]; then
    echo "❌ T3 FAILED: Rollback target ($THIRD_RELEASE) did not match previous release ($FIRST_RELEASE)."
    exit 1
fi

echo "✅ T3 PASSED."

# T4: Auto-Cleanup Limit (Pruning)
echo "[T4] Testing Auto-Cleanup Limit (Pruning)..."
sleep 1
./deploy.sh > /dev/null
sleep 1
./deploy.sh > /dev/null
sleep 1
./deploy.sh > /dev/null

COUNT2=$(ls -d "$RELEASES_DIR"/*/ 2>/dev/null | grep -cE '/[0-9]{8}_[0-9]{6}/$')
if [ "$COUNT2" -ne 3 ]; then
    echo "❌ T4 FAILED: Expected 3 releases, found $COUNT2."
    ls -l "$RELEASES_DIR"
    exit 1
fi

echo "✅ T4 PASSED."

rm -rf "$TEMP_DIR"
echo "🎉 All Blue/Green Deploy Tests Passed!"
exit 0
