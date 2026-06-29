"""测试 SchemaCompiler 统一 Schema → 各数据库 DDL。"""

import pytest
from core.schema_compiler import SchemaCompiler, UnifiedSchema


SAMPLE_SCHEMA_YAML = """
database: gotoplan
tables:
  - name: Users
    fields:
      - name: Id
        type: bigint
        primary_key: true
        auto_increment: true
        nullable: false
      - name: UserName
        type: string
        length: 100
        nullable: false
      - name: Mobile
        type: string
        length: 30
        nullable: true
      - name: CreatedAt
        type: datetime
        nullable: false

  - name: Orders
    fields:
      - name: Id
        type: bigint
        primary_key: true
        auto_increment: true
        nullable: false
      - name: UserId
        type: bigint
        nullable: false
      - name: Amount
        type: decimal
        precision: 18
        scale: 2
        nullable: false
      - name: Status
        type: tinyint
        nullable: false
      - name: CreatedAt
        type: datetime
        nullable: false
"""


@pytest.fixture
def compiler():
    return SchemaCompiler()


@pytest.fixture
def schema():
    return UnifiedSchema.from_yaml(SAMPLE_SCHEMA_YAML)


def test_schema_parses_tables(schema):
    assert len(schema.tables) == 2
    assert schema.tables[0].name == "Users"
    assert schema.tables[1].name == "Orders"


def test_schema_parses_fields(schema):
    users = schema.tables[0]
    assert len(users.fields) == 4
    id_field = users.fields[0]
    assert id_field.primary_key is True
    assert id_field.auto_increment is True


# ── SQL Server ────────────────────────────────────────────────────────────────

def test_sqlserver_uses_nvarchar(compiler, schema):
    sql = compiler.compile(schema, "sqlserver")
    assert "NVARCHAR(100)" in sql


def test_sqlserver_uses_identity(compiler, schema):
    sql = compiler.compile(schema, "sqlserver")
    assert "IDENTITY(1,1)" in sql


def test_sqlserver_uses_datetime2(compiler, schema):
    sql = compiler.compile(schema, "sqlserver")
    assert "DATETIME2" in sql


def test_sqlserver_uses_decimal(compiler, schema):
    sql = compiler.compile(schema, "sqlserver")
    assert "DECIMAL(18,2)" in sql


def test_sqlserver_create_database(compiler, schema):
    sql = compiler.compile(schema, "sqlserver")
    assert "CREATE DATABASE [gotoplan]" in sql


# ── MySQL ────────────────────────────────────────────────────────────────────

def test_mysql_uses_varchar(compiler, schema):
    sql = compiler.compile(schema, "mysql")
    assert "VARCHAR(100)" in sql


def test_mysql_uses_auto_increment(compiler, schema):
    sql = compiler.compile(schema, "mysql")
    assert "AUTO_INCREMENT" in sql


def test_mysql_uses_datetime(compiler, schema):
    sql = compiler.compile(schema, "mysql")
    assert "DATETIME" in sql


def test_mysql_create_database(compiler, schema):
    sql = compiler.compile(schema, "mysql")
    assert "CREATE DATABASE IF NOT EXISTS `gotoplan`" in sql


# ── PostgreSQL ───────────────────────────────────────────────────────────────

def test_postgresql_uses_bigserial(compiler, schema):
    sql = compiler.compile(schema, "postgresql")
    assert "BIGSERIAL" in sql


def test_postgresql_uses_varchar(compiler, schema):
    sql = compiler.compile(schema, "postgresql")
    assert "VARCHAR(100)" in sql


def test_postgresql_uses_timestamp(compiler, schema):
    sql = compiler.compile(schema, "postgresql")
    assert "TIMESTAMP" in sql


def test_postgresql_uses_numeric(compiler, schema):
    sql = compiler.compile(schema, "postgresql")
    assert "NUMERIC(18,2)" in sql


def test_postgresql_create_table_if_not_exists(compiler, schema):
    sql = compiler.compile(schema, "postgresql")
    assert "CREATE TABLE IF NOT EXISTS" in sql


# ── 跨数据库一致性 ────────────────────────────────────────────────────────────

def test_all_databases_have_users_table(compiler, schema):
    for db_type in ("sqlserver", "mysql", "postgresql"):
        sql = compiler.compile(schema, db_type)
        assert "Users" in sql, f"{db_type} 缺少 Users 表"


def test_all_databases_have_orders_table(compiler, schema):
    for db_type in ("sqlserver", "mysql", "postgresql"):
        sql = compiler.compile(schema, db_type)
        assert "Orders" in sql, f"{db_type} 缺少 Orders 表"


# ── compile_insert（seed_data）────────────────────────────────────────────────

SEED_ROWS = [
    {"UserName": "alice", "Age": 30, "Active": True, "Note": None},
    {"UserName": "bob's", "Age": 25, "Active": False, "Note": "vip"},
]


def test_compile_insert_empty_rows_returns_empty(compiler):
    assert compiler.compile_insert("Users", [], "mysql") == ""


def test_compile_insert_mysql_quoting(compiler):
    sql = compiler.compile_insert("Users", SEED_ROWS, "mysql")
    assert "INSERT INTO `Users`" in sql
    assert "`UserName`" in sql


def test_compile_insert_sqlserver_quoting_and_database(compiler):
    sql = compiler.compile_insert("Users", SEED_ROWS, "sqlserver", database="gotoplan")
    assert "INSERT INTO [gotoplan].dbo.[Users]" in sql
    assert sql.rstrip().endswith("GO")


def test_compile_insert_postgresql_switches_database(compiler):
    sql = compiler.compile_insert("Users", SEED_ROWS, "postgresql", database="gotoplan")
    assert sql.startswith('\\c "gotoplan"')
    assert 'INSERT INTO "Users"' in sql


def test_compile_insert_escapes_single_quote(compiler):
    sql = compiler.compile_insert("Users", SEED_ROWS, "mysql")
    assert "bob''s" in sql


def test_compile_insert_handles_null_and_bool(compiler):
    sql = compiler.compile_insert("Users", SEED_ROWS, "mysql")
    assert "NULL" in sql
    assert "TRUE" in sql
    assert "FALSE" in sql


def test_compile_insert_sqlserver_bool_uses_bit(compiler):
    sql = compiler.compile_insert("Users", SEED_ROWS, "sqlserver")
    assert ", 1," in sql or "(1," in sql or ", 1)" in sql


# ── compile_create_index（create_index）─────────────────────────────────────

def test_compile_create_index_empty_columns_returns_empty(compiler):
    assert compiler.compile_create_index("Users", [], "mysql") == ""


def test_compile_create_index_default_name(compiler):
    sql = compiler.compile_create_index("Users", ["Mobile"], "mysql")
    assert "idx_Users_Mobile" in sql
    assert "`Users`" in sql


def test_compile_create_index_sqlserver_qualifies_database(compiler):
    sql = compiler.compile_create_index("Users", ["Mobile"], "sqlserver", database="gotoplan")
    assert "[gotoplan].dbo.[Users]" in sql
    assert sql.rstrip().endswith("GO")


def test_compile_create_index_postgresql_if_not_exists(compiler):
    sql = compiler.compile_create_index("Users", ["Mobile"], "postgresql")
    assert "CREATE INDEX IF NOT EXISTS" in sql


def test_compile_create_index_unique(compiler):
    sql = compiler.compile_create_index("Users", ["Email"], "mysql", unique=True)
    assert "CREATE UNIQUE INDEX" in sql


def test_compile_create_index_custom_name_and_multi_column(compiler):
    sql = compiler.compile_create_index("Orders", ["UserId", "Status"], "postgresql", index_name="idx_custom")
    assert '"idx_custom"' in sql
    assert '"UserId"' in sql and '"Status"' in sql
