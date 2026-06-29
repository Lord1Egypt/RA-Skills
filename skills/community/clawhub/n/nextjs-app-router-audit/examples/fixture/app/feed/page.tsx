// Intentionally flawed fixture: a Server Component with a request waterfall
// and no metadata export. The scanner should flag `request-waterfall` (INFO)
// and `page-missing-metadata` (WARN).
export default async function FeedPage() {
  const user = await fetch("https://api.example.com/user").then((r) => r.json());
  const posts = await fetch("https://api.example.com/posts").then((r) => r.json());

  return (
    <ul>
      <li>{user.name}</li>
      {posts.map((p: { id: string; title: string }) => (
        <li key={p.id}>{p.title}</li>
      ))}
    </ul>
  );
}
