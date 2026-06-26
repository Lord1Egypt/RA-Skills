infographic sequence-interaction-wide-capsule-item
data
  title TCP三次握手
  desc 客户端与服务器建立可靠连接的过程
  sequences
    - label 客户端
      icon mingcute/computer-line
      children
        - label CLOSED
          id client-closed
          icon mingcute/close-circle-line
          step 0
        - label SYN-SENT
          id client-syn-sent
          icon mingcute/send-line
          step 2
        - label ESTABLISHED
          id client-established
          icon mingcute/check-circle-line
          step 4
    - label 服务器
      icon mingcute/server-line
      children
        - label CLOSED
          id server-closed
          icon mingcute/close-circle-line
          step 0
        - label LISTEN
          id server-listen
          icon mingcute/ear-line
          step 1
        - label SYN-RCVD
          id server-syn-rcvd
          icon mingcute/receive-line
          step 3
        - label ESTABLISHED
          id server-established
          icon mingcute/check-circle-line
          step 4
  relations
    client-closed - SYN=1, seq=x -> server-listen
    server-listen - SYN=1, ACK=1, seq=y, ack=x+1 -> client-syn-sent
    client-syn-sent - ACK=1, seq=x+1, ack=y+1 -> server-syn-rcvd
    client-established <- 数据传输 -> server-established
theme light
  palette antv