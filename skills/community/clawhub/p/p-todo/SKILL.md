# P-Todo REST API Skill

---

## 简体中文

> 当用户需要操作 P-Todo 待办应用时使用此 skill。
> 触发词：待办、任务、P-Todo、todo、task、タスク、作業、tâche、할일、Aufgabe、tarea、tarefa

**前置条件：** P-Todo 应用已启动（端口 9527），访问 `http://localhost:9527/api/health` 确认服务正常。

**端口：** 9527（可在设置页修改，修改后需重启）
**数据库：** SQLite，位于 `~/P-Todo/data/P-Todo.db`
**日志：** `~/P-Todo/data/P-Todo.log`
**支持语言：** zh, zh-TW, en, ja, ko, fr, de, es, pt

### 健康检查
```
GET /api/health
```

### 待办管理
```
GET    /api/todos              获取所有待办
GET    /api/todos/{id}         获取单个待办
POST   /api/todos              创建待办（body: {title, description, priority, assignee_id, due_date, tags}）
PUT    /api/todos/{id}         更新待办
DELETE /api/todos/{id}         删除待办
POST   /api/todos/{id}/complete 切换完成状态
```

### 评论
```
GET    /api/todos/{id}/comments  获取待办评论
POST   /api/todos/{id}/comments  添加评论（body: {user_id, content}）
DELETE /api/comments/{id}        删除评论
```

### 用户管理
```
GET    /api/users              获取所有用户
POST   /api/users              创建用户（body: {name}）
PUT    /api/users/{id}         更新用户
DELETE /api/users/{id}         删除用户
```

### 统计与搜索
```
GET    /api/stats              获取统计数据
GET    /api/search?q=keyword   搜索待办
```

### 设置
```
GET    /api/settings/sound     获取音效路径
POST   /api/settings/sound     设置音效路径（body: {soundPath}）
GET    /api/settings/language  获取当前语言
POST   /api/settings/language  切换语言（body: {language}，如 "zh"/"en"/"ja"）
POST   /api/export             导出数据（body: {format: "json"|"csv", path: "可选"}）
```

### 优先级
`LOW`（低）、`MEDIUM`（中）、`HIGH`（高）、`URGENT`（紧急）

### 调用示例
```bash
# 创建待办
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"买菜","priority":"HIGH","assignee_id":"user-001"}'

# 获取所有待办
curl http://localhost:9527/api/todos

# 切换完成状态
curl -X POST http://localhost:9527/api/todos/{id}/complete
```

---

## 繁體中文

> 當使用者需要操作 P-Todo 待辦應用時使用此 skill。
> 觸發詞：待辦、任務、P-Todo、todo、task、タスク、作業、tâche、할일、Aufgabe、tarea、tarefa

**前置條件：** P-Todo 應用已啟動（連接埠 9527），存取 `http://localhost:9527/api/health` 確認服務正常。

**連接埠：** 9527（可在設定頁修改，修改後需重啟）
**資料庫：** SQLite，位於 `~/P-Todo/data/P-Todo.db`
**日誌：** `~/P-Todo/data/P-Todo.log`
**支援語言：** zh, zh-TW, en, ja, ko, fr, de, es, pt

### 健康檢查
```
GET /api/health
```

### 待辦管理
```
GET    /api/todos              取得所有待辦
GET    /api/todos/{id}         取得單個待辦
POST   /api/todos              建立待辦（body: {title, description, priority, assignee_id, due_date, tags}）
PUT    /api/todos/{id}         更新待辦
DELETE /api/todos/{id}         刪除待辦
POST   /api/todos/{id}/complete 切換完成狀態
```

### 評論
```
GET    /api/todos/{id}/comments  取得待辦評論
POST   /api/todos/{id}/comments  新增評論（body: {user_id, content}）
DELETE /api/comments/{id}        刪除評論
```

### 使用者管理
```
GET    /api/users              取得所有使用者
POST   /api/users              建立使用者（body: {name}）
PUT    /api/users/{id}         更新使用者
DELETE /api/users/{id}         刪除使用者
```

### 統計與搜尋
```
GET    /api/stats              取得統計資料
GET    /api/search?q=keyword   搜尋待辦
```

### 設定
```
GET    /api/settings/sound     取得音效路徑
POST   /api/settings/sound     設定音效路徑（body: {soundPath}）
GET    /api/settings/language  取得目前語言
POST   /api/settings/language  切換語言（body: {language}，如 "zh"/"en"/"ja"）
POST   /api/export             匯出資料（body: {format: "json"|"csv", path: "可選"}）
```

### 優先順序
`LOW`（低）、`MEDIUM`（中）、`HIGH`（高）、`URGENT`（緊急）

### 呼叫範例
```bash
# 建立待辦
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"買菜","priority":"HIGH","assignee_id":"user-001"}'

# 取得所有待辦
curl http://localhost:9527/api/todos

# 切換完成狀態
curl -X POST http://localhost:9527/api/todos/{id}/complete
```

---

## English

> Use this skill when users need to interact with the P-Todo todo application.
> Triggers: 待办, 任务, P-Todo, todo, task, タスク, 作業, tâche, 할일, Aufgabe, tarea, tarefa

**Prerequisites:** P-Todo app must be running (port 9527). Verify with `http://localhost:9527/api/health`.

**Port:** 9527 (configurable in Settings, requires restart)
**Database:** SQLite, located at `~/P-Todo/data/P-Todo.db`
**Logs:** `~/P-Todo/data/P-Todo.log`
**Supported languages:** zh, zh-TW, en, ja, ko, fr, de, es, pt

### Health Check
```
GET /api/health
```

### Todo Management
```
GET    /api/todos              List all todos
GET    /api/todos/{id}         Get single todo
POST   /api/todos              Create todo (body: {title, description, priority, assignee_id, due_date, tags})
PUT    /api/todos/{id}         Update todo
DELETE /api/todos/{id}         Delete todo
POST   /api/todos/{id}/complete Toggle completion
```

### Comments
```
GET    /api/todos/{id}/comments  Get comments
POST   /api/todos/{id}/comments  Add comment (body: {user_id, content})
DELETE /api/comments/{id}        Delete comment
```

### User Management
```
GET    /api/users              List users
POST   /api/users              Create user (body: {name})
PUT    /api/users/{id}         Update user
DELETE /api/users/{id}         Delete user
```

### Statistics & Search
```
GET    /api/stats              Get statistics
GET    /api/search?q=keyword   Search todos
```

### Settings
```
GET    /api/settings/sound     Get sound path
POST   /api/settings/sound     Set sound path (body: {soundPath})
GET    /api/settings/language  Get current language
POST   /api/settings/language  Set language (body: {language}, e.g. "zh"/"en"/"ja")
POST   /api/export             Export data (body: {format: "json"|"csv", path: "optional"})
```

### Priority Values
`LOW`, `MEDIUM`, `HIGH`, `URGENT`

### Examples
```bash
# Create todo
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","priority":"HIGH","assignee_id":"user-001"}'

# List all todos
curl http://localhost:9527/api/todos

# Toggle completion
curl -X POST http://localhost:9527/api/todos/{id}/complete
```

---

## 日本語

> ユーザーが P-Todo タスク管理アプリと操作する際に使用してください。
> トリガー：待办、任务、P-Todo、todo、task、タスク、作業、tâche、할일、Aufgabe、tarea、tarefa

**前提条件：** P-Todo アプリが起動している必要があります（ポート 9527）。`http://localhost:9527/api/health` でサービスの正常性を確認してください。

**ポート：** 9527（設定ページで変更可能、変更後は再起動が必要）
**データベース：** SQLite、`~/P-Todo/data/P-Todo.db` に配置
**ログ：** `~/P-Todo/data/P-Todo.log`
**対応言語：** zh, zh-TW, en, ja, ko, fr, de, es, pt

### ヘルスチェック
```
GET /api/health
```

### タスク管理
```
GET    /api/todos              全タスク取得
GET    /api/todos/{id}         単一タスク取得
POST   /api/todos              タスク作成（body: {title, description, priority, assignee_id, due_date, tags}）
PUT    /api/todos/{id}         タスク更新
DELETE /api/todos/{id}         タスク削除
POST   /api/todos/{id}/complete 完了状態切替
```

### コメント
```
GET    /api/todos/{id}/comments  コメント取得
POST   /api/todos/{id}/comments  コメント追加（body: {user_id, content}）
DELETE /api/comments/{id}        コメント削除
```

### ユーザー管理
```
GET    /api/users              ユーザー一覧
POST   /api/users              ユーザー作成（body: {name}）
PUT    /api/users/{id}         ユーザー更新
DELETE /api/users/{id}         ユーザー削除
```

### 統計・検索
```
GET    /api/stats              統計データ取得
GET    /api/search?q=keyword   タスク検索
```

### 設定
```
GET    /api/settings/sound     音声パス取得
POST   /api/settings/sound     音声パス設定（body: {soundPath}）
GET    /api/settings/language  現在の言語取得
POST   /api/settings/language  言語切替（body: {language}、例："zh"/"en"/"ja"）
POST   /api/export             データエクスポート（body: {format: "json"|"csv", path: "省略可"}）
```

### 優先度
`LOW`（低）、`MEDIUM`（中）、`HIGH`（高）、`URGENT`（緊急）

### 使用例
```bash
# タスク作成
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"食材を買う","priority":"HIGH","assignee_id":"user-001"}'

# 全タスク取得
curl http://localhost:9527/api/todos

# 完了状態切替
curl -X POST http://localhost:9527/api/todos/{id}/complete
```

---

## 조선어

> 사용자가 P-Todo 할일 앱과 상호작용해야 할 때 이 스킬을 사용하세요.
> 트리거: 待办, 任务, P-Todo, todo, task, タスク, 作業, tâche, 할일, Aufgabe, tarea, tarefa

**전제 조건:** P-Todo 앱이 실행 중이어야 합니다 (포트 9527). `http://localhost:9527/api/health`에서 서비스 상태를 확인하세요.

**포트:** 9527 (설정에서 변경 가능, 변경 후 재시작 필요)
**데이터베이스:** SQLite, `~/P-Todo/data/P-Todo.db` 에 위치
**로그:** `~/P-Todo/data/P-Todo.log`
**지원 언어:** zh, zh-TW, en, ja, ko, fr, de, es, pt

### 상태 확인
```
GET /api/health
```

### 할일 관리
```
GET    /api/todos              모든 할일 목록
GET    /api/todos/{id}         단일 할일 조회
POST   /api/todos              할일 생성 (body: {title, description, priority, assignee_id, due_date, tags})
PUT    /api/todos/{id}         할일 수정
DELETE /api/todos/{id}         할일 삭제
POST   /api/todos/{id}/complete 완료 상태 전환
```

### 댓글
```
GET    /api/todos/{id}/comments  댓글 조회
POST   /api/todos/{id}/comments  댓글 추가 (body: {user_id, content})
DELETE /api/comments/{id}        댓글 삭제
```

### 사용자 관리
```
GET    /api/users              사용자 목록
POST   /api/users              사용자 생성 (body: {name})
PUT    /api/users/{id}         사용자 수정
DELETE /api/users/{id}         사용자 삭제
```

### 통계 및 검색
```
GET    /api/stats              통계 조회
GET    /api/search?q=keyword   할일 검색
```

### 설정
```
GET    /api/settings/sound     사운드 경로 조회
POST   /api/settings/sound     사운드 경로 설정 (body: {soundPath})
GET    /api/settings/language  현재 언어 조회
POST   /api/settings/language  언어 설정 (body: {language}, 예: "zh"/"en"/"ja")
POST   /api/export             데이터 내보내기 (body: {format: "json"|"csv", path: "선택사항"})
```

### 우선순위 값
`LOW` (낮음), `MEDIUM` (보통), `HIGH` (높음), `URGENT` (긴급)

### 사용 예시
```bash
# 할일 생성
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"장보기","priority":"HIGH","assignee_id":"user-001"}'

# 모든 할일 목록
curl http://localhost:9527/api/todos

# 완료 상태 전환
curl -X POST http://localhost:9527/api/todos/{id}/complete
```

---

## Français

> Utilisez cette compétence lorsque les utilisateurs ont besoin d'interagir avec l'application de tâches P-Todo.
> Déclencheurs : 待办, 任务, P-Todo, todo, task, タスク, 作業, tâche, 할일, Aufgabe, tarea, tarefa

**Prérequis :** L'application P-Todo doit être en cours d'exécution (port 9527). Vérifiez avec `http://localhost:9527/api/health`.

**Port :** 9527 (configurable dans les paramètres, redémarrage requis)
**Base de données :** SQLite, située dans `~/P-Todo/data/P-Todo.db`
**Journaux :** `~/P-Todo/data/P-Todo.log`
**Langues supportées :** zh, zh-TW, en, ja, ko, fr, de, es, pt

### Vérification de santé
```
GET /api/health
```

### Gestion des tâches
```
GET    /api/todos              Lister toutes les tâches
GET    /api/todos/{id}         Obtenir une tâche
POST   /api/todos              Créer une tâche (body: {title, description, priority, assignee_id, due_date, tags})
PUT    /api/todos/{id}         Modifier une tâche
DELETE /api/todos/{id}         Supprimer une tâche
POST   /api/todos/{id}/complete Basculer l'achèvement
```

### Commentaires
```
GET    /api/todos/{id}/comments  Obtenir les commentaires
POST   /api/todos/{id}/comments  Ajouter un commentaire (body: {user_id, content})
DELETE /api/comments/{id}        Supprimer un commentaire
```

### Gestion des utilisateurs
```
GET    /api/users              Lister les utilisateurs
POST   /api/users              Créer un utilisateur (body: {name})
PUT    /api/users/{id}         Modifier un utilisateur
DELETE /api/users/{id}         Supprimer un utilisateur
```

### Statistiques et recherche
```
GET    /api/stats              Obtenir les statistiques
GET    /api/search?q=keyword   Rechercher des tâches
```

### Paramètres
```
GET    /api/settings/sound     Obtenir le chemin du son
POST   /api/settings/sound     Définir le chemin du son (body: {soundPath})
GET    /api/settings/language  Obtenir la langue actuelle
POST   /api/settings/language  Définir la langue (body: {language}, ex: "zh"/"en"/"ja")
POST   /api/export             Exporter les données (body: {format: "json"|"csv", path: "optionnel"})
```

### Valeurs de priorité
`LOW` (Faible), `MEDIUM` (Moyen), `HIGH` (Élevé), `URGENT` (Urgent)

### Exemples
```bash
# Créer une tâche
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Acheter des courses","priority":"HIGH","assignee_id":"user-001"}'

# Lister toutes les tâches
curl http://localhost:9527/api/todos

# Basculer l'achèvement
curl -X POST http://localhost:9527/api/todos/{id}/complete
```

---

## Deutsch

> Verwenden Sie dieses Skill, wenn Benutzer mit der P-Todo-Anwendung interagieren müssen.
> Auslöser: 待办, 任务, P-Todo, todo, task, タスク, 作業, tâche, 할일, Aufgabe, tarea, tarefa

**Voraussetzungen:** Die P-Todo-Anwendung muss laufen (Port 9527). Überprüfen Sie mit `http://localhost:9527/api/health`.

**Port:** 9527 (in den Einstellungen konfigurierbar, Neustart erforderlich)
**Datenbank:** SQLite, befindet sich unter `~/P-Todo/data/P-Todo.db`
**Logs:** `~/P-Todo/data/P-Todo.log`
**Unterstützte Sprachen:** zh, zh-TW, en, ja, ko, fr, de, es, pt

### Gesundheitsprüfung
```
GET /api/health
```

### Aufgabenverwaltung
```
GET    /api/todos              Alle Auflagen auflisten
GET    /api/todos/{id}         Einzelne Aufgabe abrufen
POST   /api/todos              Aufgabe erstellen (body: {title, description, priority, assignee_id, due_date, tags})
PUT    /api/todos/{id}         Aufgabe bearbeiten
DELETE /api/todos/{id}         Aufgabe löschen
POST   /api/todos/{id}/complete Abschluss umschalten
```

### Kommentare
```
GET    /api/todos/{id}/comments  Kommentare abrufen
POST   /api/todos/{id}/comments  Kommentar hinzufügen (body: {user_id, content})
DELETE /api/comments/{id}        Kommentar löschen
```

### Benutzerverwaltung
```
GET    /api/users              Benutzer auflisten
POST   /api/users              Benutzer erstellen (body: {name})
PUT    /api/users/{id}         Benutzer bearbeiten
DELETE /api/users/{id}         Benutzer löschen
```

### Statistiken und Suche
```
GET    /api/stats              Statistiken abrufen
GET    /api/search?q=keyword   Aufgaben suchen
```

### Einstellungen
```
GET    /api/settings/sound     Soundpfad abrufen
POST   /api/settings/sound     Soundpfad festlegen (body: {soundPath})
GET    /api/settings/language  Aktuelle Sprache abrufen
POST   /api/settings/language  Sprache festlegen (body: {language}, z.B. "zh"/"en"/"ja")
POST   /api/export             Daten exportieren (body: {format: "json"|"csv", path: "optional"})
```

### Prioritätswerte
`LOW` (Niedrig), `MEDIUM` (Mittel), `HIGH` (Hoch), `URGENT` (Dringend)

### Beispiele
```bash
# Aufgabe erstellen
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Einkaufen","priority":"HIGH","assignee_id":"user-001"}'

# Alle Aufgaben auflisten
curl http://localhost:9527/api/todos

# Abschluss umschalten
curl -X POST http://localhost:9527/api/todos/{id}/complete
```

---

## Español

> Use esta habilidad cuando los usuarios necesiten interactuar con la aplicación de tareas P-Todo.
> Activadores: 待办, 任务, P-Todo, todo, task, タスク, 作業, tâche, 할일, Aufgabe, tarea, tarefa

**Requisitos previos:** La aplicación P-Todo debe estar ejecutándose (puerto 9527). Verifique con `http://localhost:9527/api/health`.

**Puerto:** 9527 (configurable en Configuración, requiere reinicio)
**Base de datos:** SQLite, ubicada en `~/P-Todo/data/P-Todo.db`
**Registros:** `~/P-Todo/data/P-Todo.log`
**Idiomas soportados:** zh, zh-TW, en, ja, ko, fr, de, es, pt

### Verificación de salud
```
GET /api/health
```

### Gestión de tareas
```
GET    /api/todos              Listar todas las tareas
GET    /api/todos/{id}         Obtener una tarea
POST   /api/todos              Crear tarea (body: {title, description, priority, assignee_id, due_date, tags})
PUT    /api/todos/{id}         Actualizar tarea
DELETE /api/todos/{id}         Eliminar tarea
POST   /api/todos/{id}/complete Alternar finalización
```

### Comentarios
```
GET    /api/todos/{id}/comments  Obtener comentarios
POST   /api/todos/{id}/comments  Añadir comentario (body: {user_id, content})
DELETE /api/comments/{id}        Eliminar comentario
```

### Gestión de usuarios
```
GET    /api/users              Listar usuarios
POST   /api/users              Crear usuario (body: {name})
PUT    /api/users/{id}         Actualizar usuario
DELETE /api/users/{id}         Eliminar usuario
```

### Estadísticas y búsqueda
```
GET    /api/stats              Obtener estadísticas
GET    /api/search?q=keyword   Buscar tareas
```

### Configuración
```
GET    /api/settings/sound     Obtener ruta de sonido
POST   /api/settings/sound     Establecer ruta de sonido (body: {soundPath})
GET    /api/settings/language  Obtener idioma actual
POST   /api/settings/language  Establecer idioma (body: {language}, ej: "zh"/"en"/"ja")
POST   /api/export             Exportar datos (body: {format: "json"|"csv", path: "opcional"})
```

### Valores de prioridad
`LOW` (Bajo), `MEDIUM` (Medio), `HIGH` (Alto), `URGENT` (Urgente)

### Ejemplos
```bash
# Crear tarea
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Comprar víveres","priority":"HIGH","assignee_id":"user-001"}'

# Listar todas las tareas
curl http://localhost:9527/api/todos

# Alternar finalización
curl -X POST http://localhost:9527/api/todos/{id}/complete
```

---

## Português

> Use esta habilidade quando os usuários precisarem interagir com o aplicativo de tarefas P-Todo.
> Ativadores: 待办, 任务, P-Todo, todo, task, タスク, 作業, tâche, 할일, Aufgabe, tarea, tarefa

**Pré-requisitos:** O aplicativo P-Todo deve estar em execução (porta 9527). Verifique com `http://localhost:9527/api/health`.

**Porta:** 9527 (configurável nas Configurações, requer reinicialização)
**Banco de dados:** SQLite, localizado em `~/P-Todo/data/P-Todo.db`
**Logs:** `~/P-Todo/data/P-Todo.log`
**Idiomas suportados:** zh, zh-TW, en, ja, ko, fr, de, es, pt

### Verificação de saúde
```
GET /api/health
```

### Gerenciamento de tarefas
```
GET    /api/todos              Listar todas as tarefas
GET    /api/todos/{id}         Obter uma tarefa
POST   /api/todos              Criar tarefa (body: {title, description, priority, assignee_id, due_date, tags})
PUT    /api/todos/{id}         Atualizar tarefa
DELETE /api/todos/{id}         Excluir tarefa
POST   /api/todos/{id}/complete Alternar conclusão
```

### Comentários
```
GET    /api/todos/{id}/comments  Obter comentários
POST   /api/todos/{id}/comments  Adicionar comentário (body: {user_id, content})
DELETE /api/comments/{id}        Excluir comentário
```

### Gerenciamento de usuários
```
GET    /api/users              Listar usuários
POST   /api/users              Criar usuário (body: {name})
PUT    /api/users/{id}         Atualizar usuário
DELETE /api/users/{id}         Excluir usuário
```

### Estatísticas e pesquisa
```
GET    /api/stats              Obter estatísticas
GET    /api/search?q=keyword   Pesquisar tarefas
```

### Configurações
```
GET    /api/settings/sound     Obter caminho do som
POST   /api/settings/sound     Definir caminho do som (body: {soundPath})
GET    /api/settings/language  Obter idioma atual
POST   /api/settings/language  Definir idioma (body: {language}, ex: "zh"/"en"/"ja")
POST   /api/export             Exportar dados (body: {format: "json"|"csv", path: "opcional"})
```

### Valores de prioridade
`LOW` (Baixo), `MEDIUM` (Médio), `HIGH` (Alto), `URGENT` (Urgente)

### Exemplos
```bash
# Criar tarefa
curl -X POST http://localhost:9527/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Comprar mantimentos","priority":"HIGH","assignee_id":"user-001"}'

# Listar todas as tarefas
curl http://localhost:9527/api/todos

# Alternar conclusão
curl -X POST http://localhost:9527/api/todos/{id}/complete
```
