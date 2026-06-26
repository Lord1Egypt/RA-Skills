#!/bin/bash
# phpmyadmin-manager — Gerencia o container phpMyAdmin via docker-compose.
#
# Uso:
#   ./run.sh start    # sobe o container phpMyAdmin
#   ./run.sh stop     # para o container
#   ./run.sh status   # mostra status e URL de acesso
#   ./run.sh open     # imprime URL de acesso
#
# Variáveis de configuração (com defaults):
#   PMA_CONTAINER        — nome do container (padrão: codai_phpmyadmin)
#   PMA_PORT             — porta no host (padrão: 8081)
#   MYSQL_CONTAINER      — hostname do MySQL na rede Docker (padrão: codai_db)
#   MYSQL_ROOT_PASSWORD  — senha root do MySQL (padrão: secret)
#   CODAI_NETWORK        — rede Docker compartilhada (padrão: nginx-proxy_net)

set -euo pipefail

ACTION="${1:-status}"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$BASE_DIR/docker-compose.yml"

PMA_CONTAINER="${PMA_CONTAINER:-codai_phpmyadmin}"
PMA_PORT="${PMA_PORT:-8081}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

is_running() {
    docker ps --filter "name=^${PMA_CONTAINER}$" --format '{{.Names}}' | grep -q "^${PMA_CONTAINER}$"
}

# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------

case "$ACTION" in

    start)
        if is_running; then
            echo "phpMyAdmin (${PMA_CONTAINER}) já está rodando → http://localhost:${PMA_PORT}"
        else
            echo "Iniciando phpMyAdmin..."
            docker compose -f "$COMPOSE_FILE" up -d
            echo "phpMyAdmin iniciado → http://localhost:${PMA_PORT}"
            echo "  Login: root / \${MYSQL_ROOT_PASSWORD:-secret}"
        fi
        ;;

    stop)
        if ! is_running; then
            echo "phpMyAdmin (${PMA_CONTAINER}) não está rodando."
        else
            echo "Parando phpMyAdmin..."
            docker compose -f "$COMPOSE_FILE" down
            echo "phpMyAdmin parado."
        fi
        ;;

    status)
        if is_running; then
            echo "phpMyAdmin (${PMA_CONTAINER})  running  → http://localhost:${PMA_PORT}"
        else
            echo "phpMyAdmin (${PMA_CONTAINER})  stopped"
            echo "  Execute: ./run.sh start"
        fi
        ;;

    open)
        echo "http://localhost:${PMA_PORT}"
        ;;

    *)
        echo "Uso: $0 {start|stop|status|open}"
        exit 1
        ;;
esac
