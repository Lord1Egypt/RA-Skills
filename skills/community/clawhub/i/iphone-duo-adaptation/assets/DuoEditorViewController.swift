import UIKit

@available(iOS 17.0, *)
final class DuoEditorViewController: UIViewController {
    private let notesField = UITextField()

    override func viewDidLoad() {
        super.viewDidLoad()
        title = String(localized: "Notes")
        view.backgroundColor = .systemBackground

        let scrollView = UIScrollView()
        scrollView.translatesAutoresizingMaskIntoConstraints = false
        scrollView.keyboardDismissMode = .interactive

        notesField.translatesAutoresizingMaskIntoConstraints = false
        notesField.placeholder = String(localized: "Notes")
        notesField.accessibilityLabel = String(localized: "Notes")
        notesField.accessibilityIdentifier = "editor.notes"
        notesField.font = .preferredFont(forTextStyle: .body)
        notesField.adjustsFontForContentSizeCategory = true
        notesField.borderStyle = .roundedRect

        view.addSubview(scrollView)
        scrollView.addSubview(notesField)

        let margins = view.layoutMarginsGuide
        let content = scrollView.contentLayoutGuide
        NSLayoutConstraint.activate([
            scrollView.leadingAnchor.constraint(equalTo: margins.leadingAnchor),
            scrollView.trailingAnchor.constraint(equalTo: margins.trailingAnchor),
            scrollView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            scrollView.bottomAnchor.constraint(equalTo: view.keyboardLayoutGuide.topAnchor),
            notesField.leadingAnchor.constraint(equalTo: content.leadingAnchor),
            notesField.trailingAnchor.constraint(equalTo: content.trailingAnchor),
            notesField.topAnchor.constraint(equalTo: content.topAnchor, constant: 16),
            notesField.bottomAnchor.constraint(equalTo: content.bottomAnchor, constant: -16),
            notesField.widthAnchor.constraint(equalTo: scrollView.frameLayoutGuide.widthAnchor),
            notesField.heightAnchor.constraint(greaterThanOrEqualToConstant: 44)
        ])

        let saveItem = UIBarButtonItem(
            title: String(localized: "Save"),
            image: UIImage(systemName: "checkmark"),
            primaryAction: UIAction { [weak self] _ in
                self?.notesField.resignFirstResponder()
            },
            menu: nil
        )
        navigationItem.rightBarButtonItem = saveItem
    }
}
