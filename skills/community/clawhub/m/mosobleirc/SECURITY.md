# Безопасность

## Никогда не коммитить

- реальные адреса квартир;
- реальные meter/item ID;
- серийные номера реальных приборов;
- `config/inventory.json`;
- `config/runtime.json`;
- `relay/yandex/inventory.json`;
- production Function URL;
- API keys и provider token;
- Authorization headers;
- SQLite DB и backups;
- reference images;
- provider API responses с персональными данными.

## Write safety

Запрещено:

- считать фото согласием на отправку;
- считать подтверждение OCR согласием на отправку;
- выполнять POST без явного подтверждения пользователя;
- выполнять blind retry после потерянного ответа;
- считать POST успешным без совпадающего read-back;
- обходить helper прямым HTTP-вызовом.

## Relay

Production Function должна оставаться private. В yandex-relay provider token хранится в окружении функции. В direct он читается только helper из локального regular-файла с правами 0600 или строже; symlink запрещён. Direct запрещает redirects с токеном. Не передавайте секреты в argv или диалог ассистента. Setup запускайте в своём терминале: секрет вводится скрыто.

Setup не выполняет login, SMS, token refresh или проверку сети. Он создаёт каталоги 0700 и файлы 0600, отказывается перезаписывать существующую настройку. Указывайте доверенный HTTPS origin: изменение provider_base_url определяет адрес отправки токена.

## Перед push/release

```bash
python3 tools/release_check.py
git status --short
git diff --cached
```

Release checker не заменяет code review, но блокирует известные runtime-файлы и типовые секреты.
