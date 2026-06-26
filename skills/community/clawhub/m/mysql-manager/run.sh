#!/bin/bash
# mysql-manager — Gerencia o container MySQL compartilhado via docker-compose.
#
# Uso:
#   ./run.sh start                   # sobe o container MySQL
#   ./run.sh stop                    # para o container (dados persistem no volume)
#   ./run.sh status                  # mostra status e lista bancos
#   ./run.sh create-db <nome>        # cria banco se não existir
#   ./run.sh drop-db <nome>          # remove banco (pede confirmação)
#   ./run.sh dump <origem> <destino> # copia banco origem → destino
#   ./run.sh list-dbs                # lista todos os bancos
#   ./run.sh wait                    # aguarda MySQL ficar pronto (útil em scripts)
#
# Variáveis de configuração (com defaults):
#   MYSQL_CONTAINER    — nome do container (padrão: codai_db)
#   MYSQL_ROOT_PASS    — senha root (padrão: secret)
#   MYSQL_MAIN_DB      — banco principal/fonte para dumps (padrão: codai_main)
#   CODAI_NETWORK      — rede Docker compartilhada (padrão: nginx-proxy_net)

set -euo pipefail

ACTION="${1:-status}"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$BASE_DIR/docker-compose.yml"

MYSQL_CONTAINER="${MYSQL_CONTAINER:-codai_db}"
# MYSQL_ROOT_PASSWORD matches the Docker env var that sets the password on init.
# MYSQL_ROOT_PASS is kept for backward compatibility; MYSQL_ROOT_PASSWORD takes precedence.
MYSQL_ROOT_PASS="${MYSQL_ROOT_PASSWORD:-${MYSQL_ROOT_PASS:-secret}}"
MYSQL_MAIN_DB="${MYSQL_MAIN_DB:-codai_main}"
if [ "$MYSQL_ROOT_PASS" = "secret" ] && [ "${ACTION:-}" != "status" ] && [ "${ACTION:-}" != "wait" ]; then
    echo "Aviso: usando senha MySQL padrão. Defina MYSQL_ROOT_PASSWORD para ambientes com dados reais."
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
    docker ps --filter "name=^${MYSQL_CONTAINER}$" --format '{{.Names}}' | grep -q "^${MYSQL_CONTAINER}$"
}

require_running() {
    if ! is_running; then
        echo "Erro: container ${MYSQL_CONTAINER} não está rodando."
        echo "      Execute: ./run.sh start"
        exit 1
    fi
}

sql() {
    docker exec "$MYSQL_CONTAINER" mysql -uroot -p"$MYSQL_ROOT_PASS" -sN "$@" 2>/dev/null
}

wait_ready() {
    echo "Aguardando MySQL ficar pronto..."
    until docker exec "$MYSQL_CONTAINER" mysqladmin ping -uroot -p"$MYSQL_ROOT_PASS" --silent 2>/dev/null; do
        sleep 2
    done
    echo "MySQL pronto."
}

# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------

case "$ACTION" in

    start)
        if is_running; then
            echo "MySQL (${MYSQL_CONTAINER}) já está rodando."
        else
            echo "Iniciando MySQL..."
            docker compose -f "$COMPOSE_FILE" up -d
            wait_ready
            echo "MySQL iniciado em localhost:${MYSQL_PORT:-3307}"
        fi
        ;;

    stop)
        if ! is_running; then
            echo "MySQL (${MYSQL_CONTAINER}) não está rodando."
        else
            echo "Parando MySQL (dados persistem no volume)..."
            docker compose -f "$COMPOSE_FILE" down
            echo "MySQL parado."
        fi
        ;;

    status)
        if is_running; then
            echo "MySQL (${MYSQL_CONTAINER})  running  → localhost:${MYSQL_PORT:-3307}"
            echo ""
            echo "Bancos:"
            sql -e "SHOW DATABASES;" | grep -v '^information_schema$\|^performance_schema$\|^sys$\|^Database$' | sed 's/^/  /'
        else
            echo "MySQL (${MYSQL_CONTAINER})  stopped"
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
        sql -e "CREATE DATABASE IF NOT EXISTS \`$DB\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        echo "Banco '$DB' pronto."
        ;;

    drop-db)
        DB="${2:-}"
        if [ -z "$DB" ]; then
            echo "Uso: $0 drop-db <nome>"
            exit 1
        fi
        validate_db_name "$DB"
        if [ "$DB" = "$MYSQL_MAIN_DB" ]; then
            echo "Erro: não é possível remover o banco principal '$MYSQL_MAIN_DB'."
            exit 1
        fi
        require_running
        read -r -p "Remover banco '$DB'? Esta ação é irreversível. [s/N] " confirm
        if [[ "$confirm" =~ ^[sS]$ ]]; then
            sql -e "DROP DATABASE IF EXISTS \`$DB\`;"
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
        table_count=$(sql -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$SRC';" || echo 0)
        if [ "$table_count" -eq 0 ]; then
            echo "Banco '$SRC' está vazio — nada a copiar."
            exit 0
        fi
        echo "Copiando $SRC → $DEST..."
        docker exec "$MYSQL_CONTAINER" \
            mysqldump -uroot -p"$MYSQL_ROOT_PASS" "$SRC" | \
        docker exec -i "$MYSQL_CONTAINER" \
            mysql -uroot -p"$MYSQL_ROOT_PASS" "$DEST"
        echo "Concluído."
        ;;

    list-dbs)
        require_running
        sql -e "SHOW DATABASES;" | grep -v '^information_schema$\|^performance_schema$\|^sys$\|^Database$'
        ;;

    *)
        echo "Uso: $0 {start|stop|status|wait|create-db|drop-db|dump|list-dbs}"
        exit 1
        ;;
esac
