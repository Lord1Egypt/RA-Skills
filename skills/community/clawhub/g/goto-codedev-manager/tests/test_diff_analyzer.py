from core.diff_analyzer import analyze_porcelain


PORCELAIN = """ M src/Domain/Entities/Customer.cs
A  src/Api/Controllers/CustomerController.cs
 M src/Application/Services/CustomerService.cs
?? src/Infrastructure/Repositories/CustomerRepository.cs
A  src/Infrastructure/Migrations/20240101_AddCustomers.cs
 D src/Old/Legacy.cs
"""


def test_categorization():
    a = analyze_porcelain(PORCELAIN)
    assert "src/Domain/Entities/Customer.cs" in a.entities
    assert "src/Api/Controllers/CustomerController.cs" in a.controllers
    assert "src/Application/Services/CustomerService.cs" in a.services
    assert "src/Infrastructure/Repositories/CustomerRepository.cs" in a.repositories
    assert "src/Infrastructure/Migrations/20240101_AddCustomers.cs" in a.migrations


def test_status_split():
    a = analyze_porcelain(PORCELAIN)
    assert "src/Api/Controllers/CustomerController.cs" in a.added
    assert "src/Infrastructure/Repositories/CustomerRepository.cs" in a.added  # untracked
    assert "src/Old/Legacy.cs" in a.deleted


def test_likely_db_change_true():
    assert analyze_porcelain(PORCELAIN).likely_db_change is True


def test_likely_db_change_false():
    a = analyze_porcelain(" M src/Api/Controllers/HomeController.cs\n")
    assert a.likely_db_change is False
