from core.schema_contract import SchemaContract
from stacks.base import EntityDef, EntityField


def _customer_entity():
    return EntityDef(
        name="Customer",
        table="Customers",
        source_file="Customer.cs",
        fields=[
            EntityField(name="Id", unified_type="bigint", primary_key=True, auto_increment=True, nullable=False),
            EntityField(name="Name", unified_type="string", length=100, nullable=False),
            EntityField(name="Email", unified_type="string", nullable=True),
        ],
    )


def test_pending_changes_shape():
    contract = SchemaContract.from_entities([_customer_entity()], feature="客户管理", database="GotoPlanDB")
    pending = contract.to_pending_changes()
    assert pending["feature"] == "客户管理"
    assert pending["database"] == "GotoPlanDB"
    change = pending["changes"][0]
    assert change["action"] == "create_table"
    assert change["table"] == "Customers"
    id_field = change["fields"][0]
    assert id_field["primaryKey"] and id_field["autoIncrement"]


def test_to_unified_schema_compatible_with_cloudserver():
    """转换结果应符合 cloudserver UnifiedSchema dict 结构（database + tables[].fields[]）。"""
    contract = SchemaContract.from_entities([_customer_entity()], feature="客户管理", database="GotoPlanDB")
    unified = contract.to_unified_schema()
    assert unified["database"] == "GotoPlanDB"
    table = unified["tables"][0]
    assert table["name"] == "Customers"
    fields = {f["name"]: f for f in table["fields"]}
    assert fields["Id"]["type"] == "bigint"
    assert fields["Id"]["primary_key"] and fields["Id"]["auto_increment"]
    assert fields["Name"]["length"] == 100
    assert fields["Email"]["nullable"] is True


def test_write_creates_db_contract(tmp_path):
    contract = SchemaContract.from_entities([_customer_entity()], feature="客户管理", database="GotoPlanDB")
    written = contract.write(str(tmp_path))
    pending = tmp_path / ".db-contract" / "pending-changes.json"
    plan = tmp_path / ".db-contract" / "migration-plan.md"
    assert pending.exists() and plan.exists()
    assert "Customers" in pending.read_text(encoding="utf-8")
