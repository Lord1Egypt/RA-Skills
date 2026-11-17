from core.config_loader import ConfigLoader, WorkspaceConfig
from stacks.dotnet.efcore import EfCoreStackAdapter

ENTITY_CS = """
using System;
using System.Collections.Generic;
namespace App.Domain.Entities;

public class Customer
{
    [Key]
    public long Id { get; set; }

    [Required]
    [MaxLength(100)]
    public string Name { get; set; }

    public string? Email { get; set; }

    public decimal Balance { get; set; }

    public DateTime CreatedAt { get; set; }

    public ICollection<Order> Orders { get; set; }
}
"""


def _adapter(config_dir):
    cfg = ConfigLoader(config_dir=config_dir).get_stack_config("dotnet")
    return EfCoreStackAdapter(stack_config=cfg)


def _ws(path):
    return WorkspaceConfig(id="ws", name="ws", path=str(path), stack="dotnet")


def test_extract_customer(config_dir, tmp_path):
    repo = tmp_path / "repo2"
    repo.mkdir()
    (repo / "Customer.cs").write_text(ENTITY_CS, encoding="utf-8")

    adapter = _adapter(config_dir)
    entities = adapter.extract_entities(_ws(repo), ["Customer.cs"])

    assert len(entities) == 1
    ent = entities[0]
    assert ent.name == "Customer"
    assert ent.table == "Customers"             # 朴素复数化
    by_name = {f.name: f for f in ent.fields}

    # 导航属性 Orders 被跳过
    assert "Orders" not in by_name
    assert set(by_name) == {"Id", "Name", "Email", "Balance", "CreatedAt"}

    assert by_name["Id"].unified_type == "bigint"
    assert by_name["Id"].primary_key and by_name["Id"].auto_increment
    assert by_name["Id"].nullable is False

    assert by_name["Name"].unified_type == "string"
    assert by_name["Name"].length == 100
    assert by_name["Name"].nullable is False    # [Required]

    assert by_name["Email"].nullable is True     # string?

    assert by_name["Balance"].unified_type == "decimal"
    assert by_name["Balance"].nullable is False  # 值类型非空

    assert by_name["CreatedAt"].unified_type == "datetime"


def test_migration_file_skipped(config_dir, tmp_path):
    repo = tmp_path / "repo3"
    (repo / "Migrations").mkdir(parents=True)
    (repo / "Migrations" / "X.cs").write_text(ENTITY_CS, encoding="utf-8")
    adapter = _adapter(config_dir)
    entities = adapter.extract_entities(_ws(repo), ["Migrations/X.cs"])
    assert entities == []
