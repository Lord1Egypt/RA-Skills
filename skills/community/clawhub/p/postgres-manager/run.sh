#!/bin/bash
# postgres-manager — Gerencia o container PostgreSQL compartilhado via docker-compose.
#
# Uso:
#   ./run.sh start                   # sobe o container PostgreSQL
#   ./run.sh stop                    # para o container (dados persistem no volume)
#   ./run.sh status                  # mostra status e lista bancos
#   ./run.sh create-db <nome>        # cria banco se não existir
#   ./run.sh drop-db <nome>          # remove banco (pede confirmação)
#   ./run.sh dump <origem> <destino> # copia banco origem → destino
#   ./run.sh list-dbs                # lista todos os bancos
#   ./run.sh wait                    # aguarda PostgreSQL ficar pronto
#   ./run.sh psql [<banco>]          # abre psql interativo
#
# Variáveis de configuração (com defaults):
#   POSTGRES_CONTAINER  — nome do container (padrão: codai_postgres)
#   POSTGRES_USER       — usuário (padrão: codai)
#   POSTGRES_PASSWORD   — senha (padrão: pgpass)
#   POSTGRES_MAIN_DB    — banco principal/fonte para dumps (padrão: codai_main)
#   POSTGRES_PORT       — porta no host (padrão: 5433)
#   CODAI_NETWORK       — rede Docker compartilhada (padrão: nginx-proxy_net)

set -euo pipefail

ACTION="${1:-status}"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$BASE_DIR/docker-compose.yml"

POSTGRES_CONTAINER="${POSTGRES_CONTAINER:-codai_postgres}"
POSTGRES_USER="${POSTGRES_USER:-codai}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-pgpass}"
POSTGRES_MAIN_DB="${POSTGRES_MAIN_DB:-codai_main}"
if [ "$POSTGRES_PASSWORD" = "pgpass" ] && [ "${ACTION:-}" != "status" ] && [ "${ACTION:-}" != "wait" ] && [ "${ACTION:-}" != "psql" ]; then
    echo "Aviso: usando senha PostgreSQL padrão. Defina POSTGRES_PASSWORD para ambientes com dados reais."
fi

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

validate_db_name() {
    local name="$1"
    if [[ ! "$name" =~ ^[a-z][a-z0-9_]{0,62}$ ]]; then
        echo "Erro: nome de banco inválido: '$name'"
        echo "      Use apenas letras minúsculas, números e underscore (ex: codai_feature)."
        exit 1
    fi
}

is_running() {
    docker ps --filter "name=^${POSTGRES_CONTAINER}$" --format '{{.Names}}' | grep -q "^${POSTGRES_CONTAINER}$"
}

require_running() {
    if ! is_running; then
        echo "Erro: container ${POSTGRES_CONTAINER} não está rodando."
        echo "      Execute: ./run.sh start"
        exit 1
    fi
}

psql_cmd() {
    docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" "$POSTGRES_CONTAINER" \
        psql -U "$POSTGRES_USER" -t -A "$@" 2>/dev/null
}

wait_ready() {
    echo "Aguardando PostgreSQL ficar pronto..."
    until docker exec "$POSTGRES_CONTAINER" pg_isready -U "$POSTGRES_USER" --quiet 2>/dev/null; do
        sleep 2
    done
    echo "PostgreSQL pronto."
}

# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------

case "$ACTION" in

    start)
        if is_running; then
            echo "PostgreSQL (${POSTGRES_CONTAINER}) já está rodando."
        else
            echo "Iniciando PostgreSQL..."
            docker compose -f "$COMPOSE_FILE" up -d
            wait_ready
            echo "PostgreSQL iniciado em localhost:${POSTGRES_PORT:-5433}"
        fi
        ;;

    stop)
        if ! is_running; then
            echo "PostgreSQL (${POSTGRES_CONTAINER}) não está rodando."
        else
            echo "Parando PostgreSQL (dados persistem no volume)..."
            docker compose -f "$COMPOSE_FILE" down
            echo "PostgreSQL parado."
        fi
        ;;

    status)
        if is_running; then
            echo "PostgreSQL (${POSTGRES_CONTAINER})  running  → localhost:${POSTGRES_PORT:-5433}"
            echo ""
            echo "Bancos:"
            psql_cmd -c "SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;" \
                | sed 's/^/  /'
        else
            echo "PostgreSQL (${POSTGRES_CONTAINER})  stopped"
            echo "  Execute: ./run.sh start"
        fi
        ;;

    wait)
        require_running
        wait_ready
        ;;

    create-db)
        DB="${2:-}"
        if [ -z "$DB" ]; then
            echo "Uso: $0 create-db <nome>"
            exit 1
        fi
        validate_db_name "$DB"
        require_running
        exists=$(psql_cmd -c "SELECT 1 FROM pg_database WHERE datname='$DB';" || echo "")
        if [ -z "$exists" ]; then
            psql_cmd -c "CREATE DATABASE \"$DB\";"
            echo "Banco '$DB' criado."
        else
            echo "Banco '$DB' já existe."
        fi
        ;;

    drop-db)
        DB="${2:-}"
        if [ -z "$DB" ]; then
            echo "Uso: $0 drop-db <nome>"
            exit 1
        fi
        validate_db_name "$DB"
        if [ "$DB" = "$POSTGRES_MAIN_DB" ]; then
            echo "Erro: não é possível remover o banco principal '$POSTGRES_MAIN_DB'."
            exit 1
        fi
        require_running
        read -r -p "Remover banco '$DB'? Esta ação é irreversível. [s/N] " confirm
        if [[ "$confirm" =~ ^[sS]$ ]]; then
            psql_cmd -c "DROP DATABASE IF EXISTS \"$DB\";"
            echo "Banco '$DB' removido."
        else
            echo "Cancelado."
        fi
        ;;

    dump)
        SRC="${2:-}"
        DEST="${3:-}"
        if [ -z "$SRC" ] || [ -z "$DEST" ]; then
            echo "Uso: $0 dump <origem> <destino>"
            exit 1
        fi
        validate_db_name "$SRC"
        validate_db_name "$DEST"
        require_running
        echo "Copiando $SRC → $DEST..."
        docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" "$POSTGRES_CONTAINER" \
            pg_dump -U "$POSTGRES_USER" -d "$SRC" | \
        docker exec -i -e PGPASSWORD="$POSTGRES_PASSWORD" "$POSTGRES_CONTAINER" \
            psql -U "$POSTGRES_USER" -d "$DEST"
        echo "Concluído."
        ;;

    list-dbs)
        require_running
        psql_cmd -c "SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;"
        ;;

    psql)
        DB="${2:-$POSTGRES_MAIN_DB}"
        validate_db_name "$DB"
        require_running
        docker exec -it -e PGPASSWORD="$POSTGRES_PASSWORD" "$POSTGRES_CONTAINER" \
            psql -U "$POSTGRES_USER" -d "$DB"
        ;;

    *)
        echo "Uso: $0 {start|stop|status|wait|create-db|drop-db|dump|list-dbs|psql}"
        exit 1
        ;;
esac
