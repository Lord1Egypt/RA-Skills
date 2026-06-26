#!/bin/bash

# ClawHub Wrapper Helper
# Usage: ./clawhub_helper.sh <command> [args...]

case "$1" in
    publish)
        # Usage: ./clawhub_helper.sh publish <path> <version> "<changelog>"
        if [ "$#" -ne 4 ]; then
            echo "Usage: ./clawhub_helper.sh publish <path> <version> <changelog>"
            exit 1
        fi
        PATH_SKILL=$2
        VERSION=$3
        CHANGELOG=$4
        SLUG=$(basename "$PATH_SKILL")
        echo "Publishing $SLUG@$VERSION..."
        clawhub publish "$PATH_SKILL" --slug "$SLUG" --name "$SLUG" --version "$VERSION" --changelog "$CHANGELOG"
        ;;
    install)
        # Usage: ./clawhub_helper.sh install <slug> [version]
        SLUG=$2
        VERSION=$3
        if [ -z "$SLUG" ]; then
            echo "Usage: ./clawhub_helper.sh install <slug> [version]"
            exit 1
        fi
        
        echo "Searching for $SLUG..."
        clawhub search "$SLUG"
        
        if [ -z "$VERSION" ]; then
            echo "Installing latest version of $SLUG..."
            clawhub install "$SLUG"
        else
            echo "Installing $SLUG version $VERSION..."
            clawhub install "$SLUG" --version "$VERSION"
        fi
        ;;
    *)
        echo "Usage: $0 {publish|install}"
        exit 1
        ;;
esac
