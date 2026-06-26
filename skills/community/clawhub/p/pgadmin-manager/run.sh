#!/bin/bash
# pgadmin-manager — Gerencia o container pgAdmin via docker-compose.
#
# Uso:
#   ./run.sh start    # sobe o container pgAdmin
#   ./run.sh stop     # para o container (configurações persistem no volume)
#   ./run.sh status   # mostra status e URL de acesso
#   ./run.sh open     # imprime URL de acesso
#
# Variáveis de configuração (com defaults):
#   PGADMIN_CONTAINER — nome do container (padrão: codai_pgadmin)
#   PGADMIN_PORT      — porta no host (padrão: 8082)
#   PGADMIN_EMAIL     — e-mail de login (padrão: admin@codai.local)
#   PGADMIN_PASSWORD  — senha de login (padrão: pgadmin)
#   CODAI_NETWORK     — rede Docker compartilhada (padrão: nginx-proxy_net)

set -euo pipefail

ACTION="${1:-status}"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$BASE_DIR/docker-compose.yml"

PGADMIN_CONTAINER="${PGADMIN_CONTAINER:-codai_pgadmin}"
PGADMIN_PORT="${PGADMIN_PORT:-8082}"
PGADMIN_EMAIL="${PGADMIN_EMAIL:-admin@codai.local}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

is_running() {
    docker ps --filter "name=^${PGADMIN_CONTAINER}$" --format '{{.Names}}' | grep -q "^${PGADMIN_CONTAINER}$"
}

# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------

case "$ACTION" in

    start)
        if is_running; then
            echo "pgAdmin (${PGADMIN_CONTAINER}) já está rodando → http://localhost:${PGADMIN_PORT}"
        else
            echo "Iniciando pgAdmin..."
            docker compose -f "$COMPOSE_FILE" up -d
            echo "pgAdmin iniciado → http://localhost:${PGADMIN_PORT}"
            echo "  Login: ${PGADMIN_EMAIL} / \${PGADMIN_PASSWORD:-pgadmin}"
            echo "  Servidor PostgreSQL: codai_postgres:5432"
        fi
        ;;

    stop)
        if ! is_running; then
            echo "pgAdmin (${PGADMIN_CONTAINER}) não está rodando."
        else
            echo "Parando pgAdmin (configurações persistem no volume)..."
            docker compose -f "$COMPOSE_FILE" down
            echo "pgAdmin parado."
        fi
        ;;

    status)
        if is_running; then
            echo "pgAdmin (${PGADMIN_CONTAINER})  running  → http://localhost:${PGADMIN_PORT}"
        else
            echo "pgAdmin (${PGADMIN_CONTAINER})  stopped"
            echo "  Execute: ./run.sh start"
        fi
        ;;

    open)
        echo "http://localhost:${PGADMIN_PORT}"
        ;;

    *)
        echo "Uso: $0 {start|stop|status|open}"
        exit 1
        ;;
esac
