# 架构模式库

> 主流 iOS 架构模式选型与模板。

## 架构选型决策

```
项目复杂度低（1-2人）? → MVVM (最通用)
    ↓ 否
需要强可测试性? → TCA (依赖注入友好)
    ↓ 否
大型团队/多模块? → VIPER (模块化最佳)
    ↓ 否
需要响应式? → MVVM + Combine
```

## MVVM 模板

```swift
// MARK: - Model
struct User: Codable, Identifiable {
    let id: Int
    let name: String
    let email: String
}

// MARK: - ViewModel
@Observable
final class UserListViewModel {
    var users: [User] = []
    var isLoading = false
    var errorMessage: String?
    
    private let repository: UserRepositoryProtocol
    
    init(repository: UserRepositoryProtocol = UserRepository()) {
        self.repository = repository
    }
    
    @MainActor
    func loadUsers() async {
        isLoading = true
        errorMessage = nil
        do {
            users = try await repository.fetchUsers()
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }
}

// MARK: - View
struct UserListView: View {
    @State private var viewModel = UserListViewModel()
    
    var body: some View {
        List(viewModel.users) { user in
            VStack(alignment: .leading) {
                Text(user.name)
                    .font(.headline)
                Text(user.email)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .task { await viewModel.loadUsers() }
        .overlay {
            if viewModel.isLoading { ProgressView() }
        }
    }
}
```

## 网络层模板

```swift
// MARK: - API Client
protocol APIEndpoint {
    var path: String { get }
    var method: HTTPMethod { get }
    var headers: [String: String] { get }
    var body: Encodable? { get }
}

final class APIClient {
    private let session: URLSession
    private let decoder: JSONDecoder
    private let baseURL: URL
    
    init(baseURL: URL, 
         session: URLSession = .shared,
         decoder: JSONDecoder = .init()) {
        self.baseURL = baseURL
        self.session = session
        self.decoder = decoder
    }
    
    func request<T: Decodable>(_ endpoint: APIEndpoint) async throws -> T {
        var request = URLRequest(url: baseURL.appendingPathComponent(endpoint.path))
        request.httpMethod = endpoint.method.rawValue
        request.allHTTPHeaderFields = endpoint.headers
        request.timeoutInterval = 10
        
        if let body = endpoint.body {
            request.httpBody = try JSONEncoder().encode(body)
        }
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw APIError.invalidResponse
        }
        
        return try decoder.decode(T.self, from: data)
    }
}

enum HTTPMethod: String {
    case GET, POST, PUT, DELETE, PATCH
}

enum APIError: LocalizedError {
    case invalidResponse
    case decodingFailed(Error)
    
    var errorDescription: String? {
        switch self {
        case .invalidResponse: return "服务器响应异常"
        case .decodingFailed: return "数据解析失败"
        }
    }
}
```

## 数据层模板 (SwiftData)

```swift
import SwiftData

@Model
final class Note {
    var id: UUID
    var title: String
    var content: String
    var createdAt: Date
    var updatedAt: Date
    var isFavorite: Bool
    
    init(title: String, content: String) {
        self.id = UUID()
        self.title = title
        self.content = content
        self.createdAt = .now
        self.updatedAt = .now
        self.isFavorite = false
    }
}

// ModelContainer
let container = try ModelContainer(for: Note.self)
let context = ModelContext(container)
```
