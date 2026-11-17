# InfinityContext — other languages

`SKILL.md` carries the two canonical sections (English and 简体中文) so that it stays
small enough for an agent to load on every turn. The localised summaries below cover the
same facts: the four Python scripts, the same safety rules and the same host support.
There is no other code in the published package.

---

# 無限上下文壓縮與記憶優化

> 壓縮上下文、把去識別化後的對話片段存到**本機** SQLite/FTS5，隨時精確檢索。

- **這是什麼**：標準 `SKILL.md` 技能，支援 dsh、Claude Code、OpenClaw、Cursor、Dify、Ollama 與自訂 Agent。
- **安裝**：`clawhub install infinitycontext --workdir ~/.agents --dir skills`；原始碼安裝需固定 tag 並校驗 `checksums.txt`（見 `SKILL.md` 的 Install）。
- **只需 Python 3.9+**：純標準庫，**不聯網、無 shell、不啟動子程序**。
- **保留期有界**：預設 30 天（`--retention-days 1..3650`）；不限時間需顯式 `--allow-unbounded-retention`；`INFINITY_CONTEXT_NO_ARCHIVE=1` 可完全關閉。
- **僅本機可讀**：目錄 0700／檔案 0600（Windows 受保護 DACL），Fail-Closed。
- **清理需二次確認**：`cleanup.py` 必須 `--apply --confirm-destructive`。
- **授權**：MIT，附強制署名條款——**必須標註 Pondsi**。

---

# 無限コンテキスト圧縮とメモリ最適化

> コンテキストを圧縮し、秘匿化した会話断片を**ローカル** SQLite/FTS5 に保存して、いつでも正確に検索。

- **概要**：標準 `SKILL.md` スキル。dsh、Claude Code、OpenClaw、Cursor、Dify、Ollama、独自エージェントに対応。
- **インストール**：`clawhub install infinitycontext --workdir ~/.agents --dir skills`。ソース導入は tag を固定して `checksums.txt` を検証（`SKILL.md` の Install を参照）。
- **Python 3.9+ のみ**：標準ライブラリのみ、**ネットワークなし・shell なし・子プロセスなし**。
- **保持期間は有界**：既定 30 日（`--retention-days 1..3650`）。無期限は `--allow-unbounded-retention` が必要。`INFINITY_CONTEXT_NO_ARCHIVE=1` で停止。
- **所有者のみ読み取り可**：ディレクトリ 0700／ファイル 0600（Windows は保護 DACL）、Fail-Closed。
- **削除は二重確認**：`cleanup.py` は `--apply --confirm-destructive` が必須。
- **ライセンス**：MIT（強制署名条項）。**Pondsi のクレジット表記が必須**。

---

# 무한 컨텍스트 압축과 메모리 최적화

> 컨텍스트를 압축하고 비식별화된 대화 조각을 **로컬** SQLite/FTS5에 저장해 언제든 정확히 검색합니다.

- **개요**: 표준 `SKILL.md` 스킬. dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama, 사용자 정의 에이전트 지원.
- **설치**: `clawhub install infinitycontext --workdir ~/.agents --dir skills`. 소스 설치는 tag 고정 후 `checksums.txt` 검증(`SKILL.md`의 Install 참조).
- **Python 3.9+만 필요**: 표준 라이브러리만, **네트워크 없음·shell 없음·하위 프로세스 없음**.
- **보존 기간은 유한**: 기본 30일(`--retention-days 1..3650`). 무제한은 `--allow-unbounded-retention` 필요. `INFINITY_CONTEXT_NO_ARCHIVE=1`로 중지.
- **소유자만 읽기 가능**: 디렉터리 0700/파일 0600(Windows는 보호 DACL), Fail-Closed.
- **삭제는 이중 확인**: `cleanup.py`는 `--apply --confirm-destructive`가 필요합니다.
- **라이선스**: MIT(필수 저작자 표시 조항). **Pondsi를 반드시 명시**.

---

# Compresión de contexto y memoria optimizada

> Comprime el contexto, guarda fragmentos anonimizados en un almacén **local** SQLite/FTS5 y recupera detalles exactos cuando los necesites.

- **Qué es**: una skill `SKILL.md` estándar para dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama y agentes propios.
- **Instalación**: `clawhub install infinitycontext --workdir ~/.agents --dir skills`; desde el código fuente, fija el tag y verifica `checksums.txt` (ver Install en `SKILL.md`).
- **Solo Python 3.9+**: biblioteca estándar, **sin red, sin shell, sin subprocesos**.
- **Retención acotada**: 30 días por defecto (`--retention-days 1..3650`); sin límite solo con `--allow-unbounded-retention`; `INFINITY_CONTEXT_NO_ARCHIVE=1` lo detiene.
- **Solo el propietario lee**: directorio 0700 / archivos 0600 (DACL protegida en Windows), fail-closed.
- **Borrado con doble confirmación**: `cleanup.py` exige `--apply --confirm-destructive`.
- **Licencia**: MIT con atribución obligatoria: **Pondsi debe figurar siempre**.

---

# Compressão de contexto e memória otimizada

> Comprime o contexto, guarda trechos anonimizados em um armazenamento **local** SQLite/FTS5 e recupera detalhes exatos quando precisar.

- **O que é**: uma skill `SKILL.md` padrão para dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama e agentes próprios.
- **Instalação**: `clawhub install infinitycontext --workdir ~/.agents --dir skills`; a partir do código-fonte, fixe a tag e verifique `checksums.txt` (ver Install em `SKILL.md`).
- **Apenas Python 3.9+**: biblioteca padrão, **sem rede, sem shell, sem subprocessos**.
- **Retenção limitada**: 30 dias por padrão (`--retention-days 1..3650`); sem limite apenas com `--allow-unbounded-retention`; `INFINITY_CONTEXT_NO_ARCHIVE=1` desliga.
- **Somente o proprietário lê**: diretório 0700 / arquivos 0600 (DACL protegida no Windows), fail-closed.
- **Exclusão com dupla confirmação**: `cleanup.py` exige `--apply --confirm-destructive`.
- **Licença**: MIT com atribuição obrigatória: **Pondsi deve ser sempre creditado**.

---

# Compression de contexte et mémoire optimisée

> Compresse le contexte, archive des fragments anonymisés dans un stockage **local** SQLite/FTS5 et retrouve des détails exacts à la demande.

- **Quoi** : une skill `SKILL.md` standard pour dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama et agents maison.
- **Installation** : `clawhub install infinitycontext --workdir ~/.agents --dir skills` ; depuis les sources, figez le tag et vérifiez `checksums.txt` (voir Install dans `SKILL.md`).
- **Python 3.9+ uniquement** : bibliothèque standard, **pas de réseau, pas de shell, pas de sous-processus**.
- **Rétention bornée** : 30 jours par défaut (`--retention-days 1..3650`) ; illimitée seulement avec `--allow-unbounded-retention` ; `INFINITY_CONTEXT_NO_ARCHIVE=1` l'arrête.
- **Lecture par le propriétaire seul** : répertoire 0700 / fichiers 0600 (DACL protégée sous Windows), fail-closed.
- **Suppression à double confirmation** : `cleanup.py` exige `--apply --confirm-destructive`.
- **Licence** : MIT avec attribution obligatoire : **Pondsi doit toujours être crédité**.

---

# Kontextkompression und optimierter Speicher

> Komprimiert den Kontext, archiviert entidentifizierte Ausschnitte in einem **lokalen** SQLite/FTS5-Speicher und ruft exakte Details auf Anfrage ab.

- **Was**: eine Standard-`SKILL.md`-Skill für dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama und eigene Agenten.
- **Installation**: `clawhub install infinitycontext --workdir ~/.agents --dir skills`; aus dem Quellcode Tag fixieren und `checksums.txt` prüfen (siehe Install in `SKILL.md`).
- **Nur Python 3.9+**: Standardbibliothek, **kein Netzwerk, keine Shell, keine Subprozesse**.
- **Begrenzte Aufbewahrung**: 30 Tage standardmäßig (`--retention-days 1..3650`); unbegrenzt nur mit `--allow-unbounded-retention`; `INFINITY_CONTEXT_NO_ARCHIVE=1` stoppt sie.
- **Nur der Eigentümer liest**: Verzeichnis 0700 / Dateien 0600 (unter Windows geschützte DACL), fail-closed.
- **Löschen nur mit doppelter Bestätigung**: `cleanup.py` verlangt `--apply --confirm-destructive`.
- **Lizenz**: MIT mit verpflichtender Namensnennung: **Pondsi muss immer genannt werden**.

---

# Сжатие контекста и оптимизация памяти

> Сжимает контекст, сохраняет обезличенные фрагменты в **локальном** SQLite/FTS5 и по запросу находит точные детали.

- **Что это**: стандартный навык `SKILL.md` для dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama и собственных агентов.
- **Установка**: `clawhub install infinitycontext --workdir ~/.agents --dir skills`; из исходников — зафиксируйте tag и проверьте `checksums.txt` (см. Install в `SKILL.md`).
- **Только Python 3.9+**: стандартная библиотека, **без сети, без shell, без подпроцессов**.
- **Ограниченное хранение**: по умолчанию 30 дней (`--retention-days 1..3650`); без ограничения — только с `--allow-unbounded-retention`; `INFINITY_CONTEXT_NO_ARCHIVE=1` останавливает архивирование.
- **Чтение только владельцем**: каталог 0700 / файлы 0600 (в Windows защищённый DACL), fail-closed.
- **Удаление с двойным подтверждением**: `cleanup.py` требует `--apply --confirm-destructive`.
- **Лицензия**: MIT с обязательным указанием авторства: **Pondsi указывается всегда**.

---

See `SKILL.md` for the authoritative English and Simplified Chinese documentation,
`references/architecture.md` for the data model and the exact file layout, and
`CHANGELOG.md` for the release history.
