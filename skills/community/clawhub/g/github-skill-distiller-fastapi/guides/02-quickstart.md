# 快速开始

**适用场景**: 已完成安装，准备创建第一个 FastAPI 应用

---

## 一、Hello World 示例

### 创建第一个应用

**AI 执行说明**: AI 可以自动生成并运行以下代码

创建文件 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### 启动开发服务器

```bash
# 方式 1：使用 fastapi CLI（推荐）
fastapi dev main.py

# 方式 2：使用 uvicorn
uvicorn main:app --reload

# 方式 3：指定主机和端口
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

**期望输出**:

```
INFO:     Will watch for changes in these directories: ['/path/to/project']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 验证 API

```bash
# 测试根路径
curl http://127.0.0.1:8000/
# 返回: {"Hello":"World"}

# 测试带参数的路径
curl "http://127.0.0.1:8000/items/5?q=somequery"
# 返回: {"item_id":5,"q":"somequery"}
```

访问交互式文档：

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

---

## 二、路径参数和查询参数

### 路径参数（Path Parameters）

路径参数通过 URL 路径传递，使用 `{变量名}` 语法：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}

# 枚举路径参数
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    return {"model_name": model_name, "message": "Have some residuals"}
```

### 查询参数（Query Parameters）

不在路径中的参数自动变为查询参数：

```python
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# 可选查询参数
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This has a long description"})
    return item
```

---

## 三、请求体（Request Body）

使用 Pydantic 模型定义请求体数据结构：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}
```

**发送 POST 请求**:

```bash
curl -X POST "http://127.0.0.1:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Foo", "price": 45.2}'
```

---

## 四、数据验证

### 字段验证

使用 `Query`、`Path`、`Body` 添加验证规则：

```python
from typing import Annotated
from fastapi import FastAPI, Query, Path

app = FastAPI()

@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="The ID of the item", ge=1)],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

### Pydantic 模型验证

```python
from pydantic import BaseModel, Field, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = Field(default=None, max_length=300)
    price: float = Field(gt=0, description="Price must be greater than zero")
    tags: list[str] = []
    image: Image | None = None
```

---

## 五、响应模型

使用 `response_model` 控制返回数据结构，过滤敏感字段：

```python
from pydantic import BaseModel, EmailStr

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    # password 字段不会出现在响应中
    return user
```

**响应状态码**:

```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

---

## 六、错误处理

### 使用 HTTPException

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

fake_items_db = {"foo": "Foo", "bar": "Bar"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=404,
            detail=f"Item '{item_id}' not found",
        )
    return {"item": fake_items_db[item_id]}
```

### 自定义异常处理器

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```

---

## 七、表单和文件上传

### 接收表单数据

```bash
pip install python-multipart
```

```python
from typing import Annotated
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    return {"username": username}
```

### 文件上传

```python
from fastapi import File, UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
    }

# 多文件上传
@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}
```

---

## 八、完整 CRUD 示例

以下是一个完整的商品管理 API 示例：

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="商品管理 API", version="1.0.0")

# 数据模型
class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

# 模拟数据库
fake_db: dict[int, Item] = {}
next_id = 1

@app.get("/items/", response_model=list[Item])
async def list_items(skip: int = 0, limit: int = 10):
    items = list(fake_db.values())
    return items[skip : skip + limit]

@app.post("/items/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    global next_id
    db_item = Item(id=next_id, **item.model_dump())
    fake_db[next_id] = db_item
    next_id += 1
    return db_item

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = Item(id=item_id, **item.model_dump())
    fake_db[item_id] = updated
    return updated

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_db[item_id]
```

---

## 九、编写测试

**AI 执行说明**: AI 可以自动生成测试代码并执行测试

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_read_item():
    response = client.get("/items/5")
    assert response.status_code == 200
    assert response.json() == {"item_id": 5, "q": None}

def test_read_item_with_query():
    response = client.get("/items/5?q=test")
    assert response.status_code == 200
    assert response.json()["q"] == "test"
```

```bash
# 运行测试
pytest test_main.py -v
```

---

## 完成确认

### 检查清单

- [ ] 成功启动开发服务器
- [ ] 浏览器访问 `/docs` 可见 Swagger UI
- [ ] GET/POST/PUT/DELETE 端点正常工作
- [ ] 数据验证错误返回正确的 422 状态码
- [ ] 测试用例通过

### 下一步

继续阅读 [高级用法](03-advanced-usage.md) 了解路由器、依赖注入、认证等进阶功能
