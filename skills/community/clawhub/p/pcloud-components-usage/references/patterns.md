# 常用模式

## 表单模式

### 搜索表单 + 表格

```tsx
import { DForm, DTable, Button, Space } from '@pointcloud/pcloud-components';

const searchItems = [
  { name: 'keyword', label: '关键词', renderType: 'input', props: { placeholder: '搜索...' } },
  { name: 'status', label: '状态', renderType: 'select',
    options: [{ label: '启用', value: 1 }, { label: '禁用', value: 0 }] },
];

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id' },
  { title: '名称', dataIndex: 'name', key: 'name' },
  { title: '状态', dataIndex: 'status', key: 'status', render: (v) => v ? '启用' : '禁用' },
];

function SearchTable() {
  const [form] = DForm.useForm();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (values) => {
    setLoading(true);
    try {
      const res = await api.list(values);
      setData(res.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <DForm
        form={form}
        items={searchItems}
        layout="inline"
        onFinish={handleSearch}
      >
        <DForm.Item>
          <Space>
            <Button type="primary" htmlType="submit">查询</Button>
            <Button onClick={() => form.resetFields()}>重置</Button>
          </Space>
        </DForm.Item>
      </DForm>
      <DTable columns={columns} dataSource={data} loading={loading} rowKey="id" />
    </div>
  );
}
```

### 表单验证

```tsx
const items = [
  {
    name: 'email',
    label: '邮箱',
    renderType: 'input',
    rules: [
      { required: true, message: '请输入邮箱' },
      { type: 'email', message: '请输入正确的邮箱格式' },
    ],
  },
  {
    name: 'phone',
    label: '手机号',
    renderType: 'input',
    rules: [
      { required: true },
      { pattern: /^1\d{10}$/, message: '请输入正确的手机号' },
    ],
  },
  {
    name: 'age',
    label: '年龄',
    renderType: 'input',
    rules: [
      { required: true },
      { type: 'number', min: 18, max: 100, message: '年龄必须在 18-100 之间' },
    ],
  },
];
```

### 动态表单项

```tsx
<DynamicFormItem
  name="members"
  min={1}
  max={5}
  items={[
    { name: 'name', label: '姓名', renderType: 'input' },
    { name: 'role', label: '角色', renderType: 'select',
      options: [{ label: '管理员', value: 'admin' }, { label: '成员', value: 'member' }] },
  ]}
  addButtonText="添加成员"
/>
```

---

## 弹窗模式

### 新增/编辑弹窗

```tsx
function EditModal({ visible, record, onCancel, onOk }) {
  const formItems = [
    { name: 'name', label: '名称', renderType: 'input', rules: [{ required: true }] },
    { name: 'desc', label: '描述', renderType: 'textarea' },
  ];

  return (
    <DModal
      open={visible}
      title={record ? '编辑' : '新增'}
      onCancel={onCancel}
      onOk={() => {
        // 获取表单值并提交
        formRef.current.validateFields().then(values => onOk(values));
      }}
    >
      <DForm
        ref={formRef}
        items={formItems}
        layout="vertical"
        initialValues={record}
      />
    </DModal>
  );
}
```

### 表单弹窗 (使用 ModalForm)

```tsx
<ModalForm
  open={open}
  title="新增"
  formProps={{ items: formItems, layout: 'vertical' }}
  onCancel={() => setOpen(false)}
  onSubmit={handleSubmit}
/>
```

---

## 表格模式

### 行选择

```tsx
const [selectedRowKeys, setSelectedRowKeys] = useState([]);

<DTable
  columns={columns}
  dataSource={data}
  rowKey="id"
  rowSelection={{
    selectedRowKeys,
    onChange: (keys) => setSelectedRowKeys(keys),
  }}
/>
```

### 排序和筛选

```tsx
const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', sorter: true },
  { title: '名称', dataIndex: 'name', key: 'name',
    filters: [
      { text: '包含A', value: 'A' },
      { text: '包含B', value: 'B' },
    ],
    onFilter: (value, record) => record.name.includes(value),
  },
];

<DTable
  columns={columns}
  dataSource={data}
  onChange={(pagination, filters, sorter) => {
    console.log('排序:', sorter);
    console.log('筛选:', filters);
  }}
/>
```

### 固定列

```tsx
const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 80, fixed: 'left' },
  { title: '姓名', dataIndex: 'name', key: 'name', width: 150 },
  { title: '邮箱', dataIndex: 'email', key: 'email', width: 200 },
  { title: '操作', key: 'action', width: 120, fixed: 'right' },
];

<DTable columns={columns} dataSource={data} scroll={{ x: 1000 }} />
```

---

## 权限模式

### 基于权限显示/隐藏

```tsx
<ConfigProvider auth={userPermissions}>
  <div>
    <AuthComponent auth="user:create">
      <Button type="primary" onClick={handleAdd}>新增</Button>
    </AuthComponent>

    <AuthComponent auth="user:edit" mode="disabled">
      <Button>编辑</Button>
    </AuthComponent>

    <AuthComponent auth="user:delete">
      <Button danger>删除</Button>
    </AuthComponent>
  </div>
</ConfigProvider>
```

---

## 加载模式

### 全屏加载

```tsx
<Loading spinning tip="加载中...">
  <MainContent />
</Loading>
```

### 局部加载

```tsx
<Loading spinning={loading} tip="提交中...">
  <Form onSubmit={handleSubmit} />
</Loading>
```

---

## 配置模式

### 全局配置

```tsx
import { ConfigProvider } from '@pointcloud/pcloud-components';

<ConfigProvider
  prefixCls="my"
  iconfontUrl="//at.alicdn.com/t/font_xxx.js"
>
  <App />
</ConfigProvider>
```

### 可配置项

- `prefixCls`: 类名前缀
- `iconfontUrl`: iconfont 图标地址
- `theme`: 主题配置