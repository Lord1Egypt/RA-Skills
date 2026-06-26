from openpyxl import Workbook


def create_workbook(filename="basic_workbook.xlsx"):
    """Create an Excel file with basic headers and sample rows."""
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Data"

    worksheet.append(["Name", "Department", "Score"])
    worksheet.append(["Alice", "Sales", 92])
    worksheet.append(["Bob", "Operations", 88])
    worksheet.append(["Cindy", "Product", 95])

    workbook.save(filename)
    print(f"Workbook '{filename}' was created successfully.")


if __name__ == "__main__":
    create_workbook()
