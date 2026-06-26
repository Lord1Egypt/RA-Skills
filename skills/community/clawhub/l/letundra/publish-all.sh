#!/bin/bash
# publish-all.sh - Публикация всех скиллов Letundra на ClawHub

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Конфигурация
VERSION="1.0.0"
SKILLS=(
    "letundra-visa"
    "letundra-news"
    "letundra-rss"
    "letundra-holidays"
    "letundra-currency"
)

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Публикация скиллов Letundra${NC}"
echo -e "${GREEN}  Версия: $VERSION${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Проверка наличия clawhub
if ! command -v clawhub &> /dev/null; then
    echo -e "${RED}ClawHub CLI не установлен.${NC}"
    echo "Установите: npm install -g clawhub"
    exit 1
fi

# Проверка аутентификации
echo -e "${YELLOW}Проверка аутентификации...${NC}"
if ! clawhub whoami &> /dev/null; then
    echo -e "${RED}Необходима аутентификация${NC}"
    echo "Выполните: clawhub login"
    exit 1
fi

echo -e "${GREEN}Аутентификация успешна!${NC}"
echo ""

# Публикация каждого скилла
for skill in "${SKILLS[@]}"; do
    echo -e "${YELLOW}Публикация $skill...${NC}"

    if [ -d "$skill" ]; then
        cd "$skill"

        # Публикация
        if clawhub publish . \
            --slug "$skill" \
            --version "$VERSION" \
            --tags "letundra,travel,news"; then
            echo -e "${GREEN}✓ $skill опубликован успешно!${NC}"
        else
            echo -e "${RED}✗ Ошибка публикации $skill${NC}"
        fi

        cd ..
    else
        echo -e "${RED}✗ Папка $skill не найдена${NC}"
    fi

    echo ""
done

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Готово!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Проверьте публикации:"
echo "  https://clawhub.ai"
echo ""
echo "Установите скиллы:"
echo "  clawhub install letundra-visa"
echo "  clawhub install letundra-news"
echo "  clawhub install letundra-rss"
echo "  clawhub install letundra-holidays"
echo "  clawhub install letundra-currency"
