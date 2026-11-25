import SwiftUI

@available(iOS 17.0, *)
struct DuoLibraryView: View {
    private enum Book: String, CaseIterable, Identifiable {
        case atlas
        case fieldNotes

        var id: Self { self }

        var title: LocalizedStringKey {
            switch self {
            case .atlas: return "Atlas"
            case .fieldNotes: return "Field Notes"
            }
        }
    }

    @State private var selection: Book?
    @State private var compactColumn: NavigationSplitViewColumn = .sidebar
    @State private var drafts: [Book: String] = [:]

    var body: some View {
        NavigationSplitView(preferredCompactColumn: $compactColumn) {
            List(Book.allCases, selection: $selection) { book in
                NavigationLink(value: book) {
                    Text(book.title)
                }
            }
            .navigationTitle("Library")
        } detail: {
            if let book = selection {
                Form {
                    TextField("Notes", text: draft(for: book), axis: .vertical)
                        .accessibilityIdentifier("library.notes")
                }
                .navigationTitle(book.title)
            } else {
                ContentUnavailableView("Select a book", systemImage: "books.vertical")
            }
        }
    }

    private func draft(for book: Book) -> Binding<String> {
        Binding(
            get: { drafts[book, default: ""] },
            set: { drafts[book] = $0 }
        )
    }
}
