#!/usr/bin/env bash
# Merges and deploys a branch.

BRANCH="$1"

if [ -z "$BRANCH" ]; then
    echo "Usage: $0 <branch>"
    exit 1
fi

if [ "$MOCK_GIT_MERGE_SUCCESS" = "true" ]; then
    echo "Mocked success for $BRANCH"
    exit 0
elif [ "$MOCK_GIT_MERGE_SUCCESS" = "false" ]; then
    echo "Mocked failure for $BRANCH"
    exit 1
fi

git checkout master
if ! git merge --no-ff "$BRANCH"; then
    echo "Merge conflict in branch $BRANCH"
    git merge --abort
    exit 1
fi

git push origin master
git branch -d "$BRANCH"
git push origin --delete "$BRANCH"

echo "Deployed successfully"
exit 0