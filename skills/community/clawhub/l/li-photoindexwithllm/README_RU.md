# 📸 PhotoIndexWithLLM — Русский

## Обзор

PhotoIndexWithLLM — интеллектуальная система индексации, анализа и поиска фотографий на основе больших моделей Vision-Language (VL).

## Быстрый старт

```bash
# Установка зависимостей
pip install requests

# Сканирование фотографий
python skill.py scan --dir /home/user/Photos

# Поиск фотографий
python skill.py search "пляж закат"

# Вывод JSON
python skill.py search "пляж" --format json
```

## Поддерживаемые платформы

- ✅ Windows 10/11
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Linux
- ✅ macOS 12+

## Поддерживаемые форматы изображений (17 типов)

| Тип | Форматы |
|-----|---------|
| Распространённые | `.jpg` `.jpeg` `.png` `.webp` `.bmp` `.tiff` `.gif` |
| iPhone/Apple | `.heic` `.heif` |
| Canon DSLR | `.cr2` |
| Nikon DSLR | `.nef` |
| Sony DSLR | `.arw` |
| Другие RAW | `.orf` `.raf` `.dng` `.rw2` `.pef` `.sr2` |

## Защита конфиденциальности

- По умолчанию используется только локальный режим
- Фотографии никогда не покидают ваш компьютер
- Удалённая передача требует подтверждения пользователя

## Полный список команд

```bash
# Сканирование фотографий
python skill.py scan --dir /home/user/Photos

# Поиск фотографий
python skill.py search "пляж закат"

# Сканирование и поиск
python skill.py scan_and_search --dir /home/user/Photos --query "пляж"

# Аннотация
python skill.py annotate --photo /photos/img001.jpg --type person --name Иван

# Обучение модели
python skill.py train

# Просмотр статистики
python skill.py stats

# Тестирование подключения
python skill.py test
```

## Контакт

**Автор**: 北京老李（beijingLL）
**ClawHub ID**: 43622283
