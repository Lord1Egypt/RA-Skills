# Collection Management — Detailed Reference

## Supported Data Types

### Scalar Types

| DataType | Notes |
|----------|-------|
| `DataType.BOOL` | Boolean |
| `DataType.INT8` / `INT16` / `INT32` / `INT64` | Integers |
| `DataType.FLOAT` / `DOUBLE` | Floating point |
| `DataType.VARCHAR` | String (requires `max_length`) |
| `DataType.JSON` | JSON object |
| `DataType.ARRAY` | Array (requires `element_type`, `max_capacity`) |

### Vector Types

| DataType | Notes |
|----------|-------|
| `DataType.FLOAT_VECTOR` | Float32 vector (requires `dim`) |
| `DataType.FLOAT16_VECTOR` | Float16 vector (requires `dim`) |
| `DataType.BFLOAT16_VECTOR` | BFloat16 vector (requires `dim`) |
| `DataType.BINARY_VECTOR` | Binary vector (requires `dim`) |
| `DataType.SPARSE_FLOAT_VECTOR` | Sparse vector (no `dim` needed) |
| `DataType.INT8_VECTOR` | Int8 vector (requires `dim`) |

## add_field Parameters

```python
schema.add_field(
    field_name="my_field",
    datatype=DataType.VARCHAR,
    is_primary=False,
    auto_id=False,
    max_length=256,          # Required for VARCHAR
    dim=768,                 # Required for vector types (except sparse)
    element_type=DataType.INT64,  # Required for ARRAY
    max_capacity=100,        # Required for ARRAY
    nullable=False,
    default_value=None,
    is_partition_key=False,
    description=""
)
```

## All Collection Operations

```python
# List all collections
collections = client.list_collections()

# Describe a collection
info = client.describe_collection(collection_name="my_collection")

# Check if collection exists
exists = client.has_collection(collection_name="my_collection")

# Rename a collection
client.rename_collection(old_name="old_name", new_name="new_name")

# Drop a collection
client.drop_collection(collection_name="my_collection")

# Truncate a collection (delete all data, keep schema and index)
client.truncate_collection(collection_name="my_collection")

# Load collection into memory (required before search/query)
client.load_collection(collection_name="my_collection")

# Release collection from memory
client.release_collection(collection_name="my_collection")

# Get load state
state = client.get_load_state(collection_name="my_collection")

# Get collection statistics
stats = client.get_collection_stats(collection_name="my_collection")
```

## Guidance

- Quick create is best for prototyping; use custom schema for production.
- A collection must be **loaded** before search or query operations.
- Before dropping a collection, confirm with the user — this deletes all data.
- Use `enable_dynamic_field=True` to allow inserting fields not defined in the schema.
- Use `truncate_collection` to clear all data while preserving the collection structure.
