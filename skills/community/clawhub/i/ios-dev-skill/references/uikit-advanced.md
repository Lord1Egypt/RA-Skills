# UIKit 进阶参考

> 来源：Apple UIKit Documentation（2026-04-23）
> https://developer.apple.com/documentation/uikit

## UICollectionView

### 基础用法

```swift
class ViewController: UIViewController {
    private var collectionView: UICollectionView!

    override func viewDidLoad() {
        super.viewDidLoad()
        setupCollectionView()
    }

    private func setupCollectionView() {
        let layout = UICollectionViewFlowLayout()
        layout.itemSize = CGSize(width: 100, height: 100)
        layout.minimumInteritemSpacing = 10
        layout.minimumLineSpacing = 10
        layout.sectionInset = UIEdgeInsets(top: 10, left: 10, bottom: 10, right: 10)

        collectionView = UICollectionView(
            frame: view.bounds,
            collectionViewLayout: layout
        )
        collectionView.backgroundColor = .systemBackground
        collectionView.delegate = self
        collectionView.dataSource = self
        collectionView.register(Cell.self, forCellWithReuseIdentifier: "Cell")
        collectionView.translatesAutoresizingMaskIntoConstraints = false

        view.addSubview(collectionView)
        NSLayoutConstraint.activate([
            collectionView.topAnchor.constraint(equalTo: view.topAnchor),
            collectionView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            collectionView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            collectionView.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])
    }
}

extension ViewController: UICollectionViewDataSource {
    func collectionView(_ collectionView: UICollectionView,
                        numberOfItemsInSection section: Int) -> Int {
        return items.count
    }

    func collectionView(_ collectionView: UICollectionView,
                        cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(
            withReuseIdentifier: "Cell", for: indexPath
        ) as! Cell
        cell.configure(with: items[indexPath.item])
        return cell
    }
}

extension ViewController: UICollectionViewDelegate {
    func collectionView(_ collectionView: UICollectionView,
                        didSelectItemAt indexPath: IndexPath) {
        // 处理选择
    }
}
```

### Compositional Layout（现代用法）

```swift
private func createLayout() -> UICollectionViewCompositionalLayout {
    // 3 列网格布局
    let itemSize = NSCollectionLayoutSize(
        widthDimension: .fractionalWidth(1/3),
        heightDimension: .fractionalHeight(1.0)
    )
    let item = NSCollectionLayoutItem(layoutSize: itemSize)
    item.contentInsets = NSDirectionalEdgeInsets(top: 8, leading: 8, bottom: 8, trailing: 8)

    let groupSize = NSCollectionLayoutSize(
        widthDimension: .fractionalWidth(1.0),
        heightDimension: .fractionalWidth(1/3)
    )
    let group = NSCollectionLayoutGroup.horizontal(layoutSize: groupSize, subitems: [item])

    let section = NSCollectionLayoutSection(group: group)
    section.contentInsets = NSDirectionalEdgeInsets(top: 16, leading: 8, bottom: 16, trailing: 8)

    return UICollectionViewCompositionalLayout(section: section)
}
```

---

## SnapKit 进阶

```swift
import SnapKit

class ViewController: UIViewController {
    private let headerView = UIView()
    private let tableView = UITableView()
    private let footerView = UIView()

    override func viewDidLoad() {
        super.viewDidLoad()
        setupViews()
        setupConstraints()
    }

    private func setupViews() {
        view.backgroundColor = .systemBackground

        headerView.backgroundColor = .systemBlue
        tableView.delegate = self
        tableView.dataSource = self
        footerView.backgroundColor = .systemGray5

        view.addSubview(headerView)
        view.addSubview(tableView)
        view.addSubview(footerView)
    }

    private func setupConstraints() {
        headerView.snp.makeConstraints { make in
            make.top.equalTo(view.safeAreaLayoutGuide)
            make.leading.trailing.equalToSuperview()
            make.height.equalTo(100)
        }

        tableView.snp.makeConstraints { make in
            make.top.equalTo(headerView.snp.bottom).offset(16)
            make.leading.trailing.equalToSuperview().inset(16)
            // 底部在 footer 之上
            make.bottom.equalTo(footerView.snp.top).offset(-16)
        }

        footerView.snp.makeConstraints { make in
            make.leading.trailing.equalToSuperview()
            make.bottom.equalTo(view.safeAreaLayoutGuide)
            make.height.equalTo(60)
        }

        // 更新约束
        headerView.snp.updateConstraints { make in
            make.height.equalTo(isExpanded ? 200 : 100)
        }

        // 重新布局动画
        UIView.animate(withDuration: 0.3) {
            self.view.layoutIfNeeded()
        }
    }
}
```

### 复杂布局示例

```swift
private func setupCardConstraints() {
    cardView.snp.makeConstraints { make in
        make.center.equalToSuperview()
        make.width.equalToSuperview().multipliedBy(0.8)
        make.height.lessThanOrEqualTo(400)
    }

    imageView.snp.makeConstraints { make in
        make.top.leading.trailing.equalToSuperview()
        make.height.equalTo(cardView.snp.width).multipliedBy(0.6)
    }

    titleLabel.snp.makeConstraints { make in
        make.top.equalTo(imageView.snp.bottom).offset(16)
        make.leading.trailing.equalToSuperview().inset(16)
    }

    descriptionLabel.snp.makeConstraints { make in
        make.top.equalTo(titleLabel.snp.bottom).offset(8)
        make.leading.trailing.equalToSuperview().inset(16)
        make.bottom.equalToSuperview().offset(-16)
    }
}
```

---

## UIStackView

```swift
// 水平栈
let hStack = UIStackView()
hStack.axis = .horizontal
hStack.spacing = 8
hStack.alignment = .center
hStack.distribution = .fillEqually

// 垂直栈
let vStack = UIStackView()
vStack.axis = .vertical
vStack.spacing = 16
vStack.alignment = .fill
vStack.distribution = .fill

// 添加视图
hStack.addArrangedSubview(avatarView)
hStack.addArrangedSubview(nameLabel)
hStack.addArrangedSubview(arrowImage)

// 设置优先级
nameLabel.setContentHuggingPriority(.defaultLow, for: .horizontal)
arrowImage.setContentHuggingPriority(.required, for: .horizontal)
```

---

## UIScrollView

```swift
let scrollView = UIScrollView()
scrollView.translatesAutoresizingMaskIntoConstraints = false
scrollView.alwaysBounceVertical = true  // 弹性滚动
scrollView.showsVerticalScrollIndicator = true

let contentView = UIView()
contentView.translatesAutoresizingMaskIntoConstraints = false

scrollView.addSubview(contentView)
view.addSubview(scrollView)

NSLayoutConstraint.activate([
    scrollView.topAnchor.constraint(equalTo: view.topAnchor),
    scrollView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
    scrollView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
    scrollView.bottomAnchor.constraint(equalTo: view.bottomAnchor),

    contentView.topAnchor.constraint(equalTo: scrollView.topAnchor),
    contentView.leadingAnchor.constraint(equalTo: scrollView.leadingAnchor),
    contentView.trailingAnchor.constraint(equalTo: scrollView.trailingAnchor),
    contentView.bottomAnchor.constraint(equalTo: scrollView.bottomAnchor),
    // 关键：内容宽度等于 scrollView
    contentView.widthAnchor.constraint(equalTo: scrollView.widthAnchor)
])

// 内容高度动态
descriptionLabel.numberOfLines = 0
descriptionLabel.snp.makeConstraints { make in
    make.top.equalToSuperview().offset(16)
    make.leading.trailing.equalToSuperview().inset(16)
    make.bottom.equalToSuperview().offset(-16)
}
```

---

## 手势识别

### 常用手势

```swift
// 点击
let tap = UITapGestureRecognizer(target: self, action: #selector(handleTap))
view.addGestureRecognizer(tap)

// 拖拽
let pan = UIPanGestureRecognizer(target: self, action: #selector(handlePan(_:)))
view.addGestureRecognizer(pan)

@objc func handlePan(_ gesture: UIPanGestureRecognizer) {
    let translation = gesture.translation(in: view)
    let velocity = gesture.velocity(in: view)

    switch gesture.state {
    case .changed:
        view.transform = CGAffineTransform(translationX: translation.x, y: translation.y)
    case .ended:
        // 弹回去动画
        UIView.animate(withDuration: 0.3) {
            view.transform = .identity
        }
    default: break
    }
}

// 缩放
let pinch = UIPinchGestureRecognizer(target: self, action: #selector(handlePinch(_:)))
view.addGestureRecognizer(pinch)

@objc func handlePinch(_ gesture: UIPinchGestureRecognizer) {
    view.transform = view.transform.scaledBy(x: gesture.scale, y: gesture.scale)
    gesture.scale = 1.0
}

// 旋转
let rotation = UIRotationGestureRecognizer(target: self, action: #selector(handleRotation(_:)))
view.addGestureRecognizer(rotation)

// 长按
let longPress = UILongPressGestureRecognizer(target: self, action: #selector(handleLongPress(_:)))
longPress.minimumPressDuration = 0.5
view.addGestureRecognizer(longPress)

// 边缘滑动（iOS 侧滑返回）
let edgePan = UIScreenEdgePanGestureRecognizer(target: self, action: #selector(handleEdgePan))
edgePan.edges = .left
view.addGestureRecognizer(edgePan)
```

### 同时识别多个手势

```swift
// 允许多个手势同时识别
tap.require(toFail: longPress)  // 点击优先于长按
```

---

## UITabBarController

```swift
class MainTabBarController: UITabBarController {
    override func viewDidLoad() {
        super.viewDidLoad()
        setupTabs()
        setupAppearance()
    }

    private func setupTabs() {
        let homeVC = UINavigationController(rootViewController: HomeViewController())
        homeVC.tabBarItem = UITabBarItem(
            title: "首页",
            image: UIImage(systemName: "house"),
            selectedImage: UIImage(systemName: "house.fill")
        )

        let searchVC = UINavigationController(rootViewController: SearchViewController())
        searchVC.tabBarItem = UITabBarItem(
            title: "搜索",
            image: UIImage(systemName: "magnifyingglass"),
            selectedImage: UIImage(systemName: "magnifyingglass")
        )

        let profileVC = UINavigationController(rootViewController: ProfileViewController())
        profileVC.tabBarItem = UITabBarItem(
            title: "我的",
            image: UIImage(systemName: "person"),
            selectedImage: UIImage(systemName: "person.fill")
        )

        viewControllers = [homeVC, searchVC, profileVC]
    }

    private func setupAppearance() {
        let appearance = UITabBarAppearance()
        appearance.configureWithOpaqueBackground()
        appearance.backgroundColor = .systemBackground
        tabBar.standardAppearance = appearance
        if #available(iOS 15.0, *) {
            tabBar.scrollEdgeAppearance = appearance
        }
        tabBar.tintColor = .systemBlue
    }
}
```

---

## 键盘处理

```swift
class FormViewController: UIViewController {
    @IBOutlet weak var scrollView: UIScrollView!
    @IBOutlet weak var emailField: UITextField!
    @IBOutlet weak var passwordField: UITextField!

    override func viewDidLoad() {
        super.viewDidLoad()
        setupKeyboardObservers()
        setupTapGesture()
    }

    private func setupKeyboardObservers() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(keyboardWillShow),
            name: UIResponder.keyboardWillShowNotification,
            object: nil
        )
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(keyboardWillHide),
            name: UIResponder.keyboardWillHideNotification,
            object: nil
        )
    }

    private func setupTapGesture() {
        let tap = UITapGestureRecognizer(target: self, action: #selector(dismissKeyboard))
        tap.cancelsTouchesInView = false
        view.addGestureRecognizer(tap)
    }

    @objc func keyboardWillShow(_ notification: Notification) {
        guard let keyboardFrame = notification.userInfo?[
            UIResponder.keyboardFrameEndUserInfoKey
        ] as? CGRect else { return }

        let contentInsets = UIEdgeInsets(
            top: 0, left: 0,
            bottom: keyboardFrame.height, right: 0
        )
        scrollView.contentInset = contentInsets
        scrollView.scrollIndicatorInsets = contentInsets
    }

    @objc func keyboardWillHide(_ notification: Notification) {
        scrollView.contentInset = .zero
        scrollView.scrollIndicatorInsets = .zero
    }

    @objc func dismissKeyboard() {
        view.endEditing(true)
    }

    deinit {
        NotificationCenter.default.removeObserver(self)
    }
}
```

---

## 自定义 UIView

```swift
class CustomCardView: UIView {
    private let titleLabel = UILabel()
    private let subtitleLabel = UILabel()
    private let iconImageView = UIImageView()

    override init(frame: CGRect) {
        super.init(frame: frame)
        setupView()
        setupConstraints()
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupView()
        setupConstraints()
    }

    private func setupView() {
        backgroundColor = .systemBackground
        layer.cornerRadius = 16
        layer.shadowColor = UIColor.black.cgColor
        layer.shadowOpacity = 0.1
        layer.shadowOffset = CGSize(width: 0, height: 2)
        layer.shadowRadius = 8

        titleLabel.font = .systemFont(ofSize: 17, weight: .semibold)
        titleLabel.textColor = .label

        subtitleLabel.font = .systemFont(ofSize: 14)
        subtitleLabel.textColor = .secondaryLabel

        iconImageView.contentMode = .scaleAspectFit
        iconImageView.tintColor = .systemBlue

        addSubview(iconImageView)
        addSubview(titleLabel)
        addSubview(subtitleLabel)
    }

    private func setupConstraints() {
        iconImageView.translatesAutoresizingMaskIntoConstraints = false
        titleLabel.translatesAutoresizingMaskIntoConstraints = false
        subtitleLabel.translatesAutoresizingMaskIntoConstraints = false

        NSLayoutConstraint.activate([
            iconImageView.leadingAnchor.constraint(equalTo: leadingAnchor, constant: 16),
            iconImageView.centerYAnchor.constraint(equalTo: centerYAnchor),
            iconImageView.widthAnchor.constraint(equalToConstant: 40),
            iconImageView.heightAnchor.constraint(equalToConstant: 40),

            titleLabel.leadingAnchor.constraint(equalTo: iconImageView.trailingAnchor, constant: 12),
            titleLabel.trailingAnchor.constraint(equalTo: trailingAnchor, constant: -16),
            titleLabel.topAnchor.constraint(equalTo: topAnchor, constant: 16),

            subtitleLabel.leadingAnchor.constraint(equalTo: titleLabel.leadingAnchor),
            subtitleLabel.trailingAnchor.constraint(equalTo: titleLabel.trailingAnchor),
            subtitleLabel.topAnchor.constraint(equalTo: titleLabel.bottomAnchor, constant: 4),
            subtitleLabel.bottomAnchor.constraint(lessThanOrEqualTo: bottomAnchor, constant: -16)
        ])
    }

    func configure(title: String, subtitle: String, icon: String) {
        titleLabel.text = title
        subtitleLabel.text = subtitle
        iconImageView.image = UIImage(systemName: icon)
    }
}
```
