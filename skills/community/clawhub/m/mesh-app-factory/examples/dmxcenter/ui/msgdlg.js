//一边输入名称，一边过滤群组的组件
export default {
data() {return {
    dlg:false,
    msg:{downmsg:'',downtime:'',setAt:'',upmsgs:[],code:''}
}},
props: {
    serviceName:{type:String,required:true},
    tags:{type:Object,required:true},
    alertDlg:{type:Object, required:true}
},
methods:{
show(code) {
    var url="/device/getmessage?code="+code;
    request({method:"GET",url:url}, this.serviceName).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        var dt=new Date();
        if(resp.data.downmsg) {
            this.msg.downmsg=resp.data.downmsg;
            dt.setTime(resp.data.setAt);
            this.msg.setAt=datetime2str(dt,true);
            if(resp.data.downtime>resp.data.setAt) {
                dt.setTime(resp.data.downtime);
                this.msg.downtime=datetime2str(dt,true);
            } else {
                this.msg.downtime=this.tags.notTaken;
            }
        } else {
            this.msg.downmsg='';
            this.msg.downtime='';
            this.msg.setAt='';
        }
        var upmsgs=[];
        if(resp.data.upmsgs) {
            for(var m of resp.data.upmsgs) {
                dt.setTime(m.at);
                upmsgs.push({msg:m.msg,at:datetime2str(dt,true)});
            }
        }
        this.msg.upmsgs=upmsgs;
        this.msg.code=code;
        this.dlg=true;
    })
}
},
template: `
<q-dialog v-model="dlg">
  <q-card style="min-width:75vw">
    <q-card-section>
      <div class="text-h6">{{msg.code}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <q-list>
      <q-item>
       <q-item-section class="text-h6">{{tags.cust.downmsg}}</q-item-section>
      </q-item>
      <q-item>
       <q-item-section>
        <q-item-label>
         <div style="max-width:70vw;overflow-wrap:break-word;word-break:normal;white-space:normal;">{{msg.downmsg}}</div>
        </q-item-label>
        <q-item-label caption>{{msg.setAt}} / {{msg.downtime}}</q-item-label>
       </q-item-section>
      </q-item>
      <q-item>
       <q-item-section class="text-h6">{{tags.cust.upmsg}}</q-item-section>
      </q-item>
      <q-item v-for="m in msg.upmsgs">
       <q-item-section>
        <q-item-label>
         <div style="max-width:70vw;overflow-wrap:break-word;word-break:normal;white-space:normal;">{{m.msg}}</div>
        </q-item-label>
        <q-item-label caption>{{m.at}}</q-item-label>
       </q-item-section>
      </q-item>
     </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>
`
}