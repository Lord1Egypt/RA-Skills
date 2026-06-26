#!/bin/bash
case "$1" in
  sync)
    echo "Syncing full GOG library..."
    gogrepo sync ~/Games/GOG/library/
    rsync -av ~/Games/GOG/saves/ user@remote:/backups/gog/saves/
    ;;
  sync-saves)
    echo "Syncing only save files..."
    rsync -av ~/Games/GOG/saves/ user@remote:/backups/gog/saves/
    ;;
  sync-config)
    CONFIG_SRC="${GOG_CONFIG_DIR:-$HOME/Games/GOG/config}"
    CONFIG_DST="${GOG_CONFIG_REMOTE:-user@remote:/backups/gog/config}"
    echo "Syncing GOG game custom configs from $CONFIG_SRC..."
    if [ ! -d "$CONFIG_SRC" ]; then
      echo "Config directory not found: $CONFIG_SRC"
      echo "Set GOG_CONFIG_DIR to your config path."
      exit 1
    fi
    rsync -av --include='*/' --include='*.ini' --include='*.cfg' \
      --include='*.json' --include='*.xml' --include='*.bind' \
      --exclude='*' "$CONFIG_SRC/" "$CONFIG_DST/"
    echo "Config sync complete."
    ;;
  list-games)
    echo "Installed GOG games:"
    ls -la ~/Games/GOG/library/
    ;;
  *)
    echo "Usage: gog-sync [sync|sync-saves|sync-config|list-games]"
    exit 1
    ;;
esac