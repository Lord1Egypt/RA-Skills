import java.sql.*;

public class VulnerableCode {
    // 硬编码凭证
    private static final String DB_PASSWORD = "admin123";
    private static final String API_KEY = "sk-1234567890abcdef";
    
    // JDBC 连接字符串泄露密码
    private static final String DB_URL = "jdbc:mysql://localhost:3306/mydb?user=root&password=secret";
    
    public void vulnerableQuery(String userInput) throws SQLException {
        Connection conn = DriverManager.getConnection(DB_URL);
        Statement stmt = conn.createStatement();
        
        // SQL 注入风险
        String query = "SELECT * FROM users WHERE name = '" + userInput + "'";
        ResultSet rs = stmt.executeQuery(query);
    }
    
    // 不安全反序列化
    public Object deserialize(byte[] data) throws Exception {
        java.io.ObjectInputStream ois = new java.io.ObjectInputStream(
            new java.io.ByteArrayInputStream(data)
        );
        return ois.readObject();
    }
    
    // XXE 风险
    public void parseXML(String xml) throws Exception {
        javax.xml.parsers.DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = dbf.newDocumentBuilder();
        builder.parse(new org.xml.sax.InputSource(new java.io.StringReader(xml)));
    }
}
