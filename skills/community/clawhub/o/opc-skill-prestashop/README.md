# OpenClaw Skill: Assistente de Vendas Virtual PrestaShop

Esta skill transforma o agente **OpenClaw** em um **Assistente de Vendas Virtual** consultivo e persuasivo, conectado diretamente aos **Web Services RESTful do PrestaShop**.

## 🚀 Funcionalidades

- **Busca de Produtos**: `buscar_produtos(termo_de_busca)`
- **Detalhes Completos**: `consultar_detalhes_produto(id_produto)` (com preços, descrição e links de imagem)
- **Verificação de Estoque em Tempo Real**: `verificar_disponibilidade(id_produto)`
- **Recomendação por Categoria**: `listar_por_categoria(id_categoria)`
- **Cache em Memória Thread-Safe**: Minimiza o consumo de API e melhora o tempo de resposta
- **Segurança Efetiva**: Permissão exclusiva de LEITURA (bloqueia requisições POST/PUT/DELETE) e mascaramento de API Key em logs

---

## ⚙️ Configuração

1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```

2. Preencha suas credenciais do PrestaShop Web Service:
   ```env
   PRESTASHOP_SHOP_URL=https://minhaloja.com.br
   PRESTASHOP_API_KEY=SUA_CHAVE_DE_API_PRESTASHOP
   PRESTASHOP_TIMEOUT=10
   PRESTASHOP_CACHE_TTL=300
   ```

---

## 🧪 Como Executar os Testes

Execute a suíte de testes unitários e de integração mockada:

```bash
python -m unittest discover tests
```

---

## 🔒 Segurança

- A skill executa estritamente métodos **GET** via RESTful API. Qualquer tentativa de alteração (`POST`, `PUT`, `DELETE`) gerará uma exceção `PrestaShopReadOnlyError`.
- As chaves de API são mascaradas de qualquer log ou pilha de exceção.
