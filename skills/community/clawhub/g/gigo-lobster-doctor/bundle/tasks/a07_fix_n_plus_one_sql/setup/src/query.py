def list_users_with_order_count(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users ORDER BY id")
    users = cur.fetchall()
    out = []
    for uid, name in users:
        cur2 = conn.cursor()
        cur2.execute("SELECT COUNT(*) FROM orders WHERE user_id = ?", (uid,))
        cnt = cur2.fetchone()[0]
        out.append({"id": uid, "name": name, "order_count": cnt})
    return out
