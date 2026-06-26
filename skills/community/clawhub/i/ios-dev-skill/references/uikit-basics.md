# UIKit 基础参考

> 来源：Apple UIKit Documentation（2026-04-23）
> https://developer.apple.com/documentation/uikit

## UIViewController

### 基础控制器

```swift
import UIKit

class MyViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBackground
    }
}
```

### 生命周期

| 方法 | 调用时机 |
|------|---------|
| viewDidLoad | 视图加载完成 |
| viewWillAppear | 即将显示 |
| viewDidAppear | 已显示 |
| viewWillDisappear | 即将消失 |
| viewDidDisappear | 已消失 |

## UIView

### 常用视图

```swift
let label = UILabel()
label.text = "Hello"
label.font = .systemFont(ofSize: 17)
label.textColor = .label

let button = UIButton(type: .system)
button.setTitle("Click", for: .normal)

let imageView = UIImageView(image: UIImage(systemName: "star"))
```

### 布局（Auto Layout）

```swift
label.translatesAutoresizingMaskIntoConstraints = false
NSLayoutConstraint.activate([
    label.centerXAnchor.constraint(equalTo: view.centerXAnchor),
    label.centerYAnchor.constraint(equalTo: view.centerYAnchor)
])
```

### SnapKit 布局

```swift
import SnapKit

view.addSubview(label)
label.snp.makeConstraints { make in
    make.center.equalToSuperview()
    make.width.equalTo(200)
}
```

## UITableView

### 数据源

```swift
class MyViewController: UIViewController, UITableViewDataSource {
    var items = ["A", "B", "C"]

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return items.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "Cell", for: indexPath)
        cell.textLabel?.text = items[indexPath.row]
        return cell
    }
}
```

### 委托

```swift
extension MyViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        // 处理点击
    }

    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 44
    }
}
```

## UINavigationController

```swift
// 推入
let detailVC = DetailViewController()
navigationController?.pushViewController(detailVC, animated: true)

// 弹出
navigationController?.popViewController(animated: true)

// 返回根
navigationController?.popToRootViewController(animated: true)
```

## UIAlertController

```swift
// Alert
let alert = UIAlertController(
    title: "标题",
    message: "消息内容",
    preferredStyle: .alert
)
alert.addAction(UIAlertAction(title: "取消", style: .cancel))
alert.addAction(UIAlertAction(title: "确认", style: .default) { _ in
    // 处理确认
})
present(alert, animated: true)

// Action Sheet
let actionSheet = UIAlertController(
    title: nil,
    message: nil,
    preferredStyle: .actionSheet
)
actionSheet.addAction(UIAlertAction(title: "选项1", style: .default))
actionSheet.addAction(UIAlertAction(title: "删除", style: .destructive))
actionSheet.addAction(UIAlertAction(title: "取消", style: .cancel))
```

## 通知与手势

### 通知中心

```swift
// 监听
NotificationCenter.default.addObserver(
    self,
    selector: #selector(handleNotification),
    name: UIApplication.didEnterBackgroundNotification,
    object: nil
)

// 发送
NotificationCenter.default.post(
    name: .myCustomNotification,
    object: nil,
    userInfo: ["key": "value"]
)

// 移除
deinit {
    NotificationCenter.default.removeObserver(self)
}
```

### 手势识别

```swift
let tap = UITapGestureRecognizer(target: self, action: #selector(handleTap))
view.addGestureRecognizer(tap)

@objc func handleTap() {
    // 处理点击
}
```

## 网络请求

### URLSession async/await

```swift
func fetchData() async throws -> Data {
    guard let url = URL(string: "https://api.example.com/data") else {
        throw URLError(.badURL)
    }
    let (data, response) = try await URLSession.shared.data(from: url)
    guard let httpResponse = response as? HTTPURLResponse,
          (200...299).contains(httpResponse.statusCode) else {
        throw URLError(.badServerResponse)
    }
    return data
}
```

### JSON 解码

```swift
struct User: Codable {
    let id: String
    let name: String
}

func decodeUsers(from data: Data) throws -> [User] {
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase
    return try decoder.decode([User].self, from: data)
}
```
